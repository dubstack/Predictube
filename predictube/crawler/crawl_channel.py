from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def emulate_action(driver):
    while True:
    	try:																				
    		button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,".//*[@id='content']/div/div[2]/div/div/div/div/button")))
    	except TimeoutException:
    		break  # no more video

    	try:
        	button.click()  # load more video
        except:
        	continue



f = open('channel_id.txt')
channelIds = f.readlines() # List of strings
f.close()

base_url = "https://www.youtube.com/user"


ofile = open('video_id.txt','w')


driver = webdriver.Firefox()
for channelId in channelIds:
	channelId = channelId.strip()
	ofile.write(channelId+"::::")
	url = base_url+'/'+channelId+'/videos?flow=list'
	driver.get(url)
	emulate_action(driver)
	print "done"
	a_tags = driver.find_elements_by_tag_name('a')
	#a_tags = driver.find_elements_by_css_selector('a[class="yt-uix-sessionlink yt-uix-tile-link  spf-link  yt-ui-ellipsis yt-ui-ellipsis-2"]')
	visited = []
	for a_tag in a_tags:
		href = a_tag.get_attribute('href')
		if href!=None and 'https://www.youtube.com/watch?v=' in href and href not in visited:
			visited.append(href)
			ofile.write(href+",")
	ofile.write("\n\n")

ofile.close()
driver.close()


