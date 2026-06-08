import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


#比賽網址
WEB = "2026TaipeiPBQOpen"
# === 報名基本資料 ===
TARGET_TIME = "20:58:43"
WCA_ID = "2023ZHUA05"
EMAIL = "calvintaiwan605@gmail.com"  # ← 改成你自己的 Email
BIRTHDAY = {
    "year": "2009",
    "month": "3",
    "day": "25"
}
#EVENT_ID = "form_event_33"  # 只報名 3x3x3
#form_event_3bld
#form_event_3fmc
#form_event_mbld

# === 啟動瀏覽器 ===

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

driver.get(f"https://cubing-tw.net/event/{WEB}/registration")
print(f"✅ 等待到 {TARGET_TIME} 開始報名...")
s = ""
while True:
    t = datetime.now().strftime("%H:%M:%S")
    if  t >= TARGET_TIME:
        break
    if  t != s:
        print(f"{t}")
    s = t 
    time.sleep(0.1)

# === 進入報名頁填 WCA ID ===
#driver.get(f"https://cubing-tw.net/event/{WEB}/registration/select")
#wait = WebDriverWait(driver, 10)
button_start = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, f'//a[contains(@href, "{WEB}/registration/select")]')
    )
)
driver.execute_script(
    "arguments[0].scrollIntoView({block: 'center'});",
    button_start
)
time.sleep(0.2)
driver.execute_script("arguments[0].click();", button_start)

# 找輸入框（不依賴隨機 ID）
print("➡️ 填入 WCA ID...")
wait = WebDriverWait(driver, 10, poll_frequency=0.1)
wca_input = wait.until(
    EC.presence_of_element_located((By.TAG_NAME, "input"))
)
wca_input.send_keys(WCA_ID)

# 等驗證結果（成功 → is-valid，失敗 → is-invalid）
for _ in range(50):
    cls = wca_input.get_attribute("class")
    if "is-valid" in cls:
        print("✅ 驗證成功")
        break
    elif "is-invalid" in cls:
        print("❌ 驗證失敗：WCA ID 錯誤")
        driver.quit()
        exit()
    time.sleep(0.1)

# 點 GO! 送出 WCA ID
driver.find_element(By.ID, "WCAID_Button").click()

# === 填寫報名表單 ===
wait.until(EC.url_contains("/registration/form"))
print("📝 進入報名表單頁面")

time.sleep(0.1)
# 生日
Select(driver.find_element(By.ID, "form_birthday_year")).select_by_visible_text(BIRTHDAY["year"])
Select(driver.find_element(By.ID, "form_birthday_month")).select_by_visible_text(BIRTHDAY["month"])
Select(driver.find_element(By.ID, "form_birthday_day")).select_by_visible_text(BIRTHDAY["day"])

# Email
driver.find_element(By.ID, "form_email").send_keys(EMAIL)

# 勾選報名項目
checkbox = driver.find_element(
    By.XPATH,
    '//input[@type="checkbox"]'
)
driver.execute_script(
    "arguments[0].scrollIntoView(true);",
    checkbox
)
time.sleep(0.1)
driver.execute_script("arguments[0].click();", checkbox)
print("勾選項目...")

# 點預覽按鈕
preview_btn = wait.until(
    EC.element_to_be_clickable((By.ID, "BTN_Preview"))
)
driver.execute_script(
    "arguments[0].scrollIntoView({block: 'center'});",
    preview_btn
)
time.sleep(0.1)
driver.execute_script("arguments[0].click();", preview_btn)
print("🔍 預覽中...")

# 間隔
time.sleep(0.1)

# 點送出按鈕
send_btn = wait.until(
    EC.element_to_be_clickable((By.ID, "BTN_Send"))
)
driver.execute_script(
    "arguments[0].scrollIntoView({block: 'center'});",
    send_btn
)
time.sleep(0.1)
driver.execute_script("arguments[0].click();", send_btn)

# === 等待送出成功頁面 ===
try:
    WebDriverWait(driver, 10).until(EC.url_contains("/payment"))
    print("🎉 報名已成功送出！請至官方網站確認名單 ✅")
except:
    print("⚠️ 報名送出後未跳轉成功，請手動確認是否完成")

# 保留畫面觀察
time.sleep(20)
driver.quit()
