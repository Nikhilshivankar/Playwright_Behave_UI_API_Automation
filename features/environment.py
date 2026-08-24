from pathlib import Path
from playwright.sync_api import sync_playwright
from config.settings import settings
from utils.logger import logger
from utils.db_helper import DatabaseHelper
from pages.login_page import LoginPage
from api.definitions.petstore_client import PetstoreClient

def before_all(context):
    """
    Hooks executed once before the entire test suite run starts.
    Initializes playwright instance and DatabaseHelper.
    """
    logger.info("--- Starting Test Execution Suite ---")
    context.playwright = sync_playwright().start()
    
    # Session scoped database helper
    context.db_helper = DatabaseHelper()
    
    # Store settings globally in context for steps to access
    context.settings = settings

def before_scenario(context, scenario):
    """
    Hooks executed before each individual scenario starts.
    Dynamically initializes Browser page (for @ui) or API client (for @api).
    """
    logger.info(f"--- Scenario Started: {scenario.name} ---")
    
    # Get all tags including feature level tags
    scenario_tags = set(scenario.tags) | set(scenario.feature.tags)
    
    # 1. UI Scenario Context Initialization
    if "ui" in scenario_tags:
        browser_type = settings.BROWSER.lower()
        headless = settings.HEADLESS
        slow_mo = settings.SLOW_MO
        
        logger.info(f"Launching Browser context: {browser_type.upper()} | Headless={headless} | SlowMo={slow_mo}ms")
        
        if browser_type == "firefox":
            context.browser = context.playwright.firefox.launch(headless=headless, slow_mo=slow_mo)
        elif browser_type == "webkit":
            context.browser = context.playwright.webkit.launch(headless=headless, slow_mo=slow_mo)
        else:
            context.browser = context.playwright.chromium.launch(headless=headless, slow_mo=slow_mo)
            
        context.browser_context = context.browser.new_context(
            viewport={"width": 1280, "height": 720},
            base_url=settings.BASE_URL
        )
        context.page = context.browser_context.new_page()
        # Instantiate LoginPage Page Object
        context.login_page = LoginPage(context.page)
        
    # 2. API Scenario Context Initialization
    if "api" in scenario_tags:
        logger.info("Initializing API Request Context")
        context.api_request_context = context.playwright.request.new_context()
        context.petstore_client = PetstoreClient(context.api_request_context, settings.API_BASE_URL)

def after_scenario(context, scenario):
    """
    Hooks executed after each individual scenario finishes.
    Captures screenshots on UI failures, closes page/browser instances, and cleans up API contexts.
    """
    logger.info(f"Scenario Finished Status: {scenario.status}")
    
    # Get all tags including feature level tags
    scenario_tags = set(scenario.tags) | set(scenario.feature.tags)

    # Capture stacktrace for failed scenarios (UI & API)
    if scenario.status == "failed" or scenario.status.name == "failed":
        error_message = "No exception message found."
        failed_step_name = "unknown"
        for step in scenario.steps:
            if step.status == "failed" or step.status.name == "failed":
                failed_step_name = step.name
                error_message = step.error_message or str(step.exception) or error_message
                break
                
        reports_dir = Path("reports/screenshots")
        reports_dir.mkdir(parents=True, exist_ok=True)
        safe_name = "".join(c for c in scenario.name if c.isalnum() or c in (" ", "_", "-")).replace(" ", "_")
        
        # Save stacktrace to file
        trace_path = reports_dir / f"fail_{safe_name}_trace.txt"
        try:
            with open(trace_path, "w", encoding="utf-8") as f:
                f.write(f"Scenario: {scenario.name}\n")
                f.write(f"Failed Step: {failed_step_name}\n")
                f.write(f"Stacktrace:\n{error_message}\n")
            logger.error(f"Scenario failure stacktrace written to: {trace_path}")
            
            # Attach stacktrace to Allure report
            import allure
            allure.attach(
                f"Scenario: {scenario.name}\nFailed Step: {failed_step_name}\n\nStacktrace:\n{error_message}",
                name=f"failure_trace_{safe_name}",
                attachment_type=allure.attachment_type.TEXT
            )
        except Exception as ex:
            logger.error(f"Failed to record failure stacktrace: {ex}")

    # 1. UI Context Teardown and Failure Captures
    if "ui" in scenario_tags:
        if hasattr(context, "page") and context.page:
            # Capture failure screenshots
            if scenario.status == "failed" or scenario.status.name == "failed":
                reports_dir = Path("reports/screenshots")
                reports_dir.mkdir(parents=True, exist_ok=True)
                safe_name = "".join(c for c in scenario.name if c.isalnum() or c in (" ", "_", "-")).replace(" ", "_")
                screenshot_path = reports_dir / f"fail_{safe_name}.png"
                
                try:
                    context.page.screenshot(path=str(screenshot_path))
                    logger.error(f"UI Scenario failure detected. Saved screenshot to: {screenshot_path}")
                    
                    # Attach screenshot to Allure report
                    import allure
                    allure.attach.file(
                        source=str(screenshot_path),
                        name=f"failure_screenshot_{safe_name}",
                        attachment_type=allure.attachment_type.PNG
                    )
                except Exception as e:
                    logger.error(f"Failed to capture screenshot: {e}")
            
            context.page.close()
            
        if hasattr(context, "browser_context") and context.browser_context:
            context.browser_context.close()
            
        if hasattr(context, "browser") and context.browser:
            context.browser.close()
            
    # 2. API Context Teardown
    if "api" in scenario_tags:
        if hasattr(context, "api_request_context") and context.api_request_context:
            context.api_request_context.dispose()
            
    logger.info(f"--- Scenario Completed: {scenario.name} ({scenario.status.name}) ---")

def after_all(context):
    """
    Hooks executed once after the entire test suite run completes.
    Stops Playwright driver session.
    """
    logger.info("--- Cleaning up Playwright Execution session ---")
    if hasattr(context, "playwright") and context.playwright:
        context.playwright.stop()
    logger.info("--- All Test Executions Finished ---")
