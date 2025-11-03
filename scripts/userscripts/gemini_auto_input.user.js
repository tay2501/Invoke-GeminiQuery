// ==UserScript==
// @name         Gemini Auto Input
// @namespace    http://tampermonkey.net/
// @version      1.0.0
// @description  Automatic input for Google Gemini AI from command line using URL parameters
// @author       GeminiAutoQuery Team
// @match        https://aistudio.google.com/prompts/new_chat*
// @match        https://aistudio.google.com/app/prompts/new_chat*
// @match        https://aistudio.google.com/*
// @grant        none
// @run-at       document-idle
// @license      MIT
// @homepage     https://github.com/your-repo/gemini-auto-query
// ==/UserScript==

(function() {
    'use strict';
    
    /**
     * Gemini Auto Input - Greasemonkey Script
     * 
     * This script automatically fills and submits prompts to Google Gemini AI
     * based on URL parameters passed from the command line tool.
     * 
     * Features:
     * - Reads 'prompt' parameter from URL
     * - Automatically fills textarea with the prompt
     * - Clicks the submit button when ready
     * - Provides debug interface for testing
     */
    
    // Configuration constants
    const CONFIG = {
        SCRIPT_NAME: 'Gemini Auto Input',
        VERSION: '1.0.0',
        DELAY_BEFORE_START: 1000,
        ELEMENT_SEARCH_TIMEOUT: 15000,
        ELEMENT_SEARCH_INTERVAL: 100,
        BUTTON_WAIT_DELAY: 500
    };
    
    // Logging utility
    const Logger = {
        log: (message, level = 'INFO') => {
            const timestamp = new Date().toISOString().substring(11, 19);
            console.log(`[${timestamp}] [${CONFIG.SCRIPT_NAME}] [${level}] ${message}`);
        },
        
        info: (message) => Logger.log(message, 'INFO'),
        debug: (message) => Logger.log(message, 'DEBUG'),
        warn: (message) => Logger.log(message, 'WARN'),
        error: (message) => Logger.log(message, 'ERROR')
    };
    
    Logger.info(`${CONFIG.SCRIPT_NAME} v${CONFIG.VERSION} started`);
    
    // Wait for page to be fully loaded before starting
    setTimeout(() => {
        Logger.debug("Starting initialization after delay");
        initializeScript();
    }, CONFIG.DELAY_BEFORE_START);
    
    /**
     * Initialize the script and start the auto-input process
     */
    function initializeScript() {
        try {
            // Extract prompt from URL parameters
            const prompt = extractPromptFromURL();
            
            if (!prompt) {
                Logger.info("No prompt parameter found in URL - exiting");
                return;
            }
            
            Logger.info(`Found prompt: ${prompt.substring(0, 100)}...`);
            
            // Start the fill and submit process
            fillAndSubmitPrompt(prompt);
            
        } catch (error) {
            Logger.error(`Initialization failed: ${error.message}`);
        }
    }
    
    /**
     * Extract prompt from URL parameters
     * @returns {string|null} The prompt text or null if not found
     */
    function extractPromptFromURL() {
        Logger.debug(`Current URL: ${window.location.href}`);
        Logger.debug(`Search params: ${window.location.search}`);
        
        const urlParams = new URLSearchParams(window.location.search);
        
        // Debug: Log all parameters
        Logger.debug("All URL parameters:");
        for (const [key, value] of urlParams.entries()) {
            Logger.debug(`  ${key}: ${value}`);
        }
        
        // Try different parameter names
        const paramNames = ['prompt', 'q', 'data', 'text'];
        for (const paramName of paramNames) {
            const value = urlParams.get(paramName);
            if (value && value.trim()) {
                Logger.debug(`Found prompt in parameter '${paramName}'`);
                return value.trim();
            }
        }
        
        Logger.debug(`No prompt found in parameters: ${Array.from(urlParams.keys())}`);
        return null;
    }
    
    /**
     * Generic element finder with timeout
     * @param {string} selector - CSS selector to find
     * @param {number} timeout - Timeout in milliseconds
     * @returns {Promise<Element|null>} Found element or null
     */
    function findElement(selector, timeout = CONFIG.ELEMENT_SEARCH_TIMEOUT) {
        return new Promise(resolve => {
            Logger.debug(`Searching for element: ${selector}`);
            
            const interval = setInterval(() => {
                const element = document.querySelector(selector);
                if (element) {
                    Logger.debug(`Found element: ${selector}`);
                    clearInterval(interval);
                    resolve(element);
                }
            }, CONFIG.ELEMENT_SEARCH_INTERVAL);
            
            setTimeout(() => {
                clearInterval(interval);
                Logger.error(`Timeout searching for: ${selector}`);
                resolve(null);
            }, timeout);
        });
    }
    
    /**
     * Fill the textarea and submit the prompt
     * @param {string} prompt - The prompt text to fill
     */
    async function fillAndSubmitPrompt(prompt) {
        try {
            // Find the textarea element
            Logger.debug("Searching for textarea element");
            const textarea = await findElement('textarea');
            
            if (!textarea) {
                Logger.error("Could not find textarea element");
                return;
            }
            
            // Fill the textarea with the prompt
            Logger.info("Filling textarea with prompt");
            textarea.value = prompt;
            textarea.dispatchEvent(new Event('input', { bubbles: true }));
            Logger.debug("Textarea filled and input event dispatched");
            
            // Wait a moment before looking for submit button
            setTimeout(async () => {
                await findAndClickSubmitButton();
            }, CONFIG.BUTTON_WAIT_DELAY);
            
        } catch (error) {
            Logger.error(`Fill and submit failed: ${error.message}`);
        }
    }
    
    /**
     * Find and click the submit button
     */
    async function findAndClickSubmitButton() {
        Logger.debug("Searching for submit button");
        
        // Try multiple selectors for the submit button
        const buttonSelectors = [
            'button:has(.run-button-content)',  // Primary selector
            'button[aria-label*="Run"]',        // Aria label
            'button[type="submit"]',            // Submit type
            'button:contains("Run")',           // Text content
            '.run-button',                      // Class name
            'button'                            // Fallback
        ];
        
        let submitButton = null;
        
        for (const selector of buttonSelectors) {
            submitButton = await findElement(selector, 3000); // Shorter timeout per selector
            if (submitButton) {
                Logger.debug(`Found submit button with selector: ${selector}`);
                break;
            }
        }
        
        if (!submitButton) {
            Logger.error("Could not find submit button with any selector");
            return;
        }
        
        // Check if button is disabled and wait if necessary
        if (submitButton.disabled) {
            Logger.warn("Submit button is disabled - waiting for it to become enabled");
            await waitForButtonEnabled(submitButton);
        }
        
        // Click the button
        try {
            submitButton.click();
            Logger.info("Submit button clicked successfully");
        } catch (error) {
            Logger.error(`Failed to click submit button: ${error.message}`);
        }
    }
    
    /**
     * Wait for button to become enabled
     * @param {Element} button - The button element to monitor
     */
    async function waitForButtonEnabled(button) {
        const maxAttempts = 100; // 10 seconds at 100ms intervals
        let attempts = 0;
        
        return new Promise((resolve) => {
            const checkInterval = setInterval(() => {
                attempts++;
                
                if (!button.disabled) {
                    clearInterval(checkInterval);
                    Logger.debug("Button became enabled");
                    resolve();
                } else if (attempts >= maxAttempts) {
                    clearInterval(checkInterval);
                    Logger.warn("Button remained disabled after timeout");
                    resolve();
                }
            }, 100);
        });
    }
    
    // ========================================
    // Debug Interface
    // ========================================
    
    /**
     * Create debug interface for manual testing
     */
    window.geminiDebug = {
        version: CONFIG.VERSION,
        
        /**
         * Manual test with custom text
         * @param {string} customText - Custom text to test with
         */
        test: function(customText) {
            const text = customText || extractPromptFromURL() || 'Test question';
            Logger.info(`Manual test with text: "${text}"`);
            fillAndSubmitPrompt(text);
        },
        
        /**
         * Show help information
         */
        help: function() {
            console.log(`=== ${CONFIG.SCRIPT_NAME} v${CONFIG.VERSION} Help ===`);
            console.log('window.geminiDebug.test("question") - Manual test execution');
            console.log('window.geminiDebug.help() - Show this help');
            console.log('Usage: Add ?prompt=your_question to URL');
        },
        
        /**
         * Get current configuration
         */
        getConfig: function() {
            return CONFIG;
        }
    };
    
    Logger.debug("Debug interface created");
    
})();