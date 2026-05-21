## Apply

**Automatically submits the bootloader unlock permission request to Mi Community.**

### Installation & Execution

```bash
pip install miapply

```
Then just run it from anywhere using:
```bash
miapply

```
### How It Works
Xiaomi opens a limited daily quota at exactly **00:00 Beijing Time (GMT+8)**.
This script automates the submission process, sending your request automatically.
When you run the script, it will ask you to enter a **delay in milliseconds**.
The ideal delay depends on several factors, including your network speed, network type, and server response time. The goal is not to send the request exactly at 00:00, but to ensure it reaches the server’s processing stage **precisely at 00:00**.
You may need to experiment — a delay of **2500ms**, **1000ms**, or even **200ms** might work best for you. There is no universal perfect delay.
Xiaomi accepts only a very limited number of requests per day, and thousands of users compete at the same moment. Therefore, success also depends on luck.
### Important Notes
 * **Termux:** Set **Battery & Data usage** to **"Unrestricted"** and enable **Wakelock** to prevent the system from killing the process. You can do this by running:
```bash
  termux-wake-lock

```
*Or simply pull down your notification drawer and tap **"Acquire wakelock"** on the Termux notification.*
 * **PC:** Make sure your device does not enter **Sleep** or **Hibernate** mode while waiting.
### ⚠️ Crucial: Avoiding Account Restrictions (Bans)
Xiaomi's security system is highly sensitive to network and IP alterations. If the system flags your connection as unstable or suspicious, your account will be temporarily restricted, showing the following error:
> **"Account Error Please try again after MM/DD"**
> 
To prevent this temporary ban, strictly follow these guidelines before and during the process:
 * **Do NOT Switch Networks:** Never switch between Wi-Fi and Mobile Data (SIM) close to the quota reset time.
 * **Turn Off VPNs & Proxies:** Ensure all VPN applications are completely disconnected.
 * **Disable Custom DNS:** Avoid using private or custom DNS configurations that might mask or alter your network routing.
 * **Stay on One Connection:** Keep your device connected to a single, stable network provider throughout the entire execution.
### Disclaimer
Please use this script on one account only. Using it on multiple accounts to claim extra slots is unfair to other users.
```
