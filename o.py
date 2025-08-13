import time
from seleniumbase import SB

def fancy_log(message, char='-', length=40):
    print(f"{char * length}\n{message}\n{char * length}")

def handle_captcha(driver, wait_time=4):
    fancy_log("Attempting to click CAPTCHA GUI...")
    driver.uc_gui_click_captcha()
    time.sleep(1)
    fancy_log("Handling CAPTCHA GUI...")
    driver.uc_gui_handle_captcha()
    time.sleep(wait_time)

def accept_button_flow(driver, reconnect_time=4):
    if driver.is_element_present('button:contains("Accept")'):
        fancy_log("Accept button found. Clicking...")
        driver.uc_click('button:contains("Accept")', reconnect_time=reconnect_time)

def main():
    url = "https://kick.com/brutalles"
    fancy_log("Launching undetectable browser with test mode enabled!", "*")

    with SB(uc=True, test=True) as loganwai:
        fancy_log(f"Opening URL: {url}")
        loganwai.uc_open_with_reconnect(url, 4)
        time.sleep(4)
        handle_captcha(loganwai)
        accept_button_flow(loganwai)
        fancy_log("Checking for injected channel player...", "#")
        if loganwai.is_element_visible('#injected-channel-player'):
            fancy_log("Injected channel player detected. Spawning secondary driver...", "=")
            loganwai2 = loganwai.get_new_driver(undetectable=True)
            loganwai2.uc_open_with_reconnect(url, 5)
            handle_captcha(loganwai2, wait_time=4)
            accept_button_flow(loganwai2)
            fancy_log("Monitoring channel player visibility...", "~")
            while loganwai.is_element_visible('#injected-channel-player'):
                fancy_log("Channel player still visible, waiting 10s...", ".")
                time.sleep(10)
            fancy_log("Quitting extra driver...", "^")
            loganwai.quit_extra_driver()
        time.sleep(1)
        fancy_log("Script completed successfully!", "+")

if __name__ == "__main__":
    main()
