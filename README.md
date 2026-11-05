# 🎙️ Python Voice Assistant

A beginner-friendly Python Voice Assistant that listens to voice commands, understands user requests, and responds using speech. This project uses SpeechRecognition and pyttsx3, along with APIs, to perform useful daily tasks.

## 🚀 Features

- 🎤 **Speech Recognition** – Recognises spoken English commands.
- 🔊 **Text-to-Speech** – Responds using a computer-generated voice.
- 👋 **Greetings** – Responds to basic greetings.
- 🕒 **Time and Date** – Announces the current time and date.
- 🌦️ **Weather Information** – Fetches current weather details for a city using Open-Meteo API.
- 🌐 **Google Search** – Searches the web using voice commands.
- ▶️ **Open Websites** – Opens Google and YouTube.
- ⏰ **Reminders** – Sets simple reminders while the assistant is running.
- 🧠 **Question Answering** – Uses WolframAlpha API for supported factual questions.
- ⚠️ **Error Handling** – Handles microphone, network, and API errors.

## 🛠️ Technologies Used

- Python 3.13
- SpeechRecognition
- PyAudio
- pyttsx3
- Requests
- Python-dotenv
- Open-Meteo API
- WolframAlpha API (optional)

## 📁 Project Structure

```text
PythonProject6/
│
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the Project

```bash
cd PythonProject6
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

**Windows:**

```powershell
.venv\Scripts\activate
```

### 5. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file:

```env
WOLFRAM_APP_ID=
```

WolframAlpha is optional. Add your App ID to enable factual question answering.

### 7. Run the Application

```bash
python main.py
```

## 🎯 Example Voice Commands

| Voice Command | Action |
|---|---|
| Hello | Greets the user |
| What is the time? | Announces current time |
| What is today's date? | Announces today's date |
| Weather in Chennai | Provides current weather |
| Open Google | Opens Google |
| Open YouTube | Opens YouTube |
| Search for Python tutorials | Searches Google |
| Remind me to drink water in 2 minutes | Sets a reminder |
| Ask what is the capital of India | Queries WolframAlpha |
| Help | Lists available commands |
| Goodbye | Closes the assistant |

## 🔐 API Information

- **Open-Meteo:** Provides weather information without requiring an API key.
- **WolframAlpha:** Optional API integration for answering supported questions. An App ID is required.

Never upload your `.env` file or private API credentials to GitHub.

## ⚠️ Requirements

- Python 3.13 recommended.
- Working microphone and speakers.
- Internet connection for speech recognition and API requests.
- Microphone permission enabled in Windows.

## 📚 Learning Outcomes

Through this project, I learned:

- Python functions and modules.
- Speech recognition and voice processing.
- Text-to-speech implementation.
- API integration using Requests.
- Exception handling.
- Regular expressions.
- Background threading for reminders.
- Python virtual environments and package management.

## 👨‍💻 Author

**Saro**

GitHub: [Your GitHub Profile](https://github.com/simplelife277)

## ⭐ Support

If you find this project useful, please give the repository a star!

---

**Built with Python ❤️**