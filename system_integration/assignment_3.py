# Importing required libraries
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
import time
import re

# Setting up the webdriver
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_CA'})
driver = webdriver.Chrome(options=options)

# Navigating to the YouTube.ca homepage
driver.get("https://www.youtube.ca")

# Maximizing the window to prevent YouTube issues when searching
driver.maximize_window()

# Identifying the language
language = driver.find_element(By.XPATH, "//html").get_attribute('lang')
match_language = re.match(language, 'en(\_[a-z]{2})?', re.IGNORECASE)
if match_language is None:
    raise Exception('It was not possible to set the language properly')

####################################################################
# Defining the regular expressions (regex) used within the program #
####################################################################
# Regex for views count: must be over a million
REGEX_VIEWS_COUNT = r"(\d+(\.\d+)?)[mM]\s?"
# Regex for playlist size: assumes formatting as "0 / 0" or "0/0"
REGEX_PLAYLIST_SIZE = r"\d+\s?/\s?(\d+)"

# Waiting for the search input to be available
XPATH_SEARCH_INPUT = '//input[@id="search"]'
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, XPATH_SEARCH_INPUT)))

# Submitting query to be searched
search_input = driver.find_element(By.XPATH, XPATH_SEARCH_INPUT)
search_input.send_keys("selenium python")
search_input.send_keys(Keys.RETURN)

# Waiting for the results to be loaded
time.sleep(5)

# Initializing variables
miniplayer = None
playlist_size = 0
video_elements: list[WebElement] = []

# For each video in the result list, include it in the playlist
for video_container_element in driver.find_elements(By.TAG_NAME, 'ytd-video-renderer'):
    video_metadata_lines = video_container_element\
        .find_element(By.ID, 'metadata-line')\
            .find_elements(By.CLASS_NAME, 'inline-metadata-item')
    
    # Iterating over the video metadata and trying to match the number of views
    for metadata_line in video_metadata_lines:
        match_views = re.match(REGEX_VIEWS_COUNT, metadata_line.text)
        if match_views is not None:
            video_elements.append(video_container_element)
            # Printing the video data (title and views count)
            video_title_text = video_container_element.find_element(By.ID, 'video-title').text
            print(video_title_text, match_views.group(1))

# For each video picked up, include it in the playlist
for video_container in video_elements:
    # Scrolling to the video element
    ActionChains(driver).scroll_to_element(video_container).perform()
    
    # Scrolling the height of the element to prevent the action menu from being hidden 
    vertical_scroll = video_container.rect['height']
    driver.execute_script("window.scrollBy(0, {0});".format(vertical_scroll))
    
    # Changing the background color to highlight the video under control
    driver.execute_script("arguments[0].setAttribute('style', 'background-color: yellow;')", video_container)

    # Clicking on the action menu for the video
    menu_element = video_container.find_element(By.TAG_NAME, 'ytd-menu-renderer')
    menu_element.click()
    
    # Waiting for the action menu to be displayed
    time.sleep(2)
    
    # Clicking on "Add to Queue" button
    XPATH_ADD_TO_QUEUE = '//*[@id="items"]/ytd-menu-service-item-renderer[1]'
    add_to_queue_button = driver.find_element(By.XPATH, XPATH_ADD_TO_QUEUE)
    add_to_queue_button.click()
    
    # Waiting for the miniplayer to be displayed
    time.sleep(2)
    
    # Finding the miniplayer element
    miniplayer = driver.find_element(By.TAG_NAME, 'ytd-miniplayer')
    
    # Clicking on the button to expand/show the playlist
    miniplayer_expand_button = miniplayer\
        .find_element(By.ID, 'info-bar')\
            .find_element(By.CLASS_NAME, 'expander')\
                .find_element(By.ID, 'button')
    miniplayer_expand_button.click()
    
    # Waiting for the playlist expansion to be completed
    time.sleep(2)
    
    # Clicking on the button to collapse/hide the playlist
    miniplayer_expand_button.click()
    
    # Waiting for the playlist collapse to be completed
    time.sleep(2)

# Closing the miniplayer
if miniplayer is not None:
    # Finding the element that contains the playlist size
    miniplayer_playlist_size_element = miniplayer.find_element(By.XPATH, '//*[@id="info-bar"]/div[1]/div/div/span[2]')
    match_size = re.match(REGEX_PLAYLIST_SIZE, miniplayer_playlist_size_element.text)
    
    # Extracting the playlist size
    playlist_size = match_size.group(1)
    
    # Clicking on the button to close the miniplayer
    miniplayer_close_button = miniplayer.find_element(By.CLASS_NAME, 'ytp-miniplayer-close-button')
    miniplayer_close_button.click()
    
    # Waiting for the playlist closing to be completed
    time.sleep(2)
    
    # For playlists with 2 or more videos queued, it is necessary to confirm closing it
    confirmation_dialog = driver.find_element(By.TAG_NAME, 'yt-confirm-dialog-renderer')
    if confirmation_dialog is not None:
        confirmation_button = confirmation_dialog.find_element(By.ID, 'confirm-button')
        confirmation_button.click()
        
        # Waiting for the confirmation dialog to be completed
        time.sleep(2)

# Asserting that all videos were included in the playlist
assert len(video_elements) == int(playlist_size)

# Closing the webdriver
driver.close()