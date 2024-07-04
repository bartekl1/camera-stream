# 📹 Camera Stream

![GitHub release (latest by date)](https://img.shields.io/github/v/release/bartekl1/camera-stream?style=flat-square)
![GitHub Repo stars](https://img.shields.io/github/stars/bartekl1/camera-stream?style=flat-square)
![GitHub watchers](https://img.shields.io/github/watchers/bartekl1/camera-stream?style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/bartekl1/camera-stream?style=flat-square)

<!-- [🇵🇱 Polish version of README](README_PL.md) -->

## 👨‍💻 Installation

1. Clone repository

    ```bash
    git clone https://github.com/bartekl1/camera-stream
    cd camera-stream
    ```

2. Create configuration file named `configs.json` with the following content.

    ```json
    {
        "host": "0.0.0.0"
    }
    ```

3. Install PIP dependencies.

    ```bash
    pip install -r requirements.txt
    ```

4. Copy service template and replace `<PATH>` with absolute path to repository directory and `<USERNAME>` with your system username.

    ```bash
    sudo cp camera.service /etc/systemd/system/camera.service
    sudo nano /etc/systemd/system/camera.service
    ```

5. Start and enable service.

    ```bash
    sudo systemctl start camera
    sudo systemctl enable camera
    ```
