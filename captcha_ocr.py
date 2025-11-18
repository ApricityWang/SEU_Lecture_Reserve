from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import base64
import os

# 设置 Selenium WebDriver 选项
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")

# 启动 WebDriver
driver = webdriver.Chrome(options=chrome_options)

# 访问网页
url = "https://ehall.seu.edu.cn/gsapp/sys/yddjzxxtjappseu/*default/index.do#/hdyy"
driver.get(url)

# 等待页面加载
time.sleep(5)  # 页面加载时间，可根据实际情况调整

# 输入一卡通号和密码
card_number = ""
password = ""

driver.find_element(By.CLASS_NAME, "input-username-pc").find_element(By.TAG_NAME, "input").send_keys(card_number)
driver.find_element(By.CLASS_NAME, "input-password-pc").find_element(By.TAG_NAME, "input").send_keys(password)

# 点击登录按钮
driver.find_element(By.CLASS_NAME, "login-button-pc").click()

# 等待页面加载
time.sleep(5)

# 点击预约按钮
driver.find_element(By.CLASS_NAME, "ydd-button-small.button-success").click()

# 等待验证码页面加载
time.sleep(3)

# 确保 /images 目录存在
if not os.path.exists("image_dataset"):
    os.makedirs("image_dataset")

# 循环保存 100 张验证码图片
for i in range(1001):
    try:
        # 找到验证码图片
        vcode_img = driver.find_element(By.ID, "vcodeImg")
        src = vcode_img.get_attribute("src")

        if "base64," in src:
            # 提取 base64 编码部分
            base64_data = src.split("base64,")[1]
            img_data = base64.b64decode(base64_data)

            # 保存验证码图片
            img_path = f"image_dataset/captcha_{i+1+323}.jpg"
            with open(img_path, "wb") as f:
                f.write(img_data)
            print(f"Saved: {img_path}")

            # 点击验证码刷新
            ActionChains(driver).move_to_element(vcode_img).click().perform()

            # 等待 2 秒后继续
            time.sleep(1)
        else:
            print(f"第 {i+1} 次未获取到验证码")
    except Exception as e:
        print(f"错误发生：{e}")

# 关闭 WebDriver
driver.quit()
print("验证码采集完成！")