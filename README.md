# QuizU 📚

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.22%2B-red)

QuizU is an AI-powered quiz generation platform designed to transform study materials into engaging quizzes. Using Google's Gemini models, QuizU creates personalized quiz questions from your documents or text, making studying more interactive and effective.

## 🔗 Live Demo

Try QuizU now by following this [link](https://quiz-u.streamlit.app/)!

## ✨ Features

- **AI-Powered Quiz Generation**: Creates customized quizzes based on your study materials
- **Multiple File Formats**: Upload PDF, DOCX, or TXT files for processing
- **Direct Text Input**: Paste text directly for quick quiz creation
- **Question Type Selection**: Choose between Multiple Choice and True/False questions
- **Interactive Quiz Interface**: Take quizzes with immediate feedback
- **Progress Tracking**: See your score as you complete questions
- **Customizable Settings**: Control the number and types of questions

## 💡 How It Works

1. **Upload Materials**: Submit your study documents (PDF, DOCX, or TXT)
2. **Configure Quiz**: Choose question types and quantity
3. **Generate Questions**: AI analyzes your content and creates relevant questions
4. **Take Quiz**: Test your knowledge with the generated quiz
5. **Get Feedback**: Receive immediate results and explanations

## 🚀 Getting Started

### Online Usage

Visit [https://quiz-u.streamlit.app/](https://quiz-u.streamlit.app/) to use QuizU without installation.

### Local Installation

To run QuizU locally:

1. Clone the repository:

   ```bash
   git clone https://github.com/albertopuliga/QuizU.git
   cd QuizU
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Google API key:

   - Create a `.env` file in the project root
   - Add your Google Generative AI API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```
   - For instructions on getting an API key, visit [Google AI Studio](https://makersuite.google.com/)

4. Run the application:
   ```bash
   streamlit run src/app.py
   ```

## 🧩 Use Cases

- **Students**: Transform class notes into quiz questions
- **Teachers**: Create quick assessments from course materials
- **Self-learners**: Test comprehension of any subject matter
- **Study Groups**: Share quizzes based on shared reading materials

## 💻 Technology Stack

- **Frontend & Backend**: Streamlit
- **AI Generation**: Google Generative AI (Gemini models)
- **Document Processing**: PyPDF2, python-docx

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 👥 Inspiration

This project was inspired by friend [Daniel](https://github.com/RestartDK)'s version of this concept, which you can find [here](https://mintlearn.vercel.app/).

Let me know which one you like more!

## 📧 Contact

[Alberto Puliga - Github](https://github.com/albertopuliga)
