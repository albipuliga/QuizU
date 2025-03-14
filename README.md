# QuizU

QuizU is an AI-powered quiz platform that uses natural language processing (NLP) and machine learning algorithms to generate personalized quizzes for users. The platform allows users to create quizzes, select questions, and receive instant feedback on their answers.

## Features
- AI-powered quiz generation
- User-friendly interface
- Support for multiple file formats (txt, pdf, docx)
- Option to enter text directly
- Customizable number of questions
- Display of correct answers and explanations
- Option to save quizzes for future reference

## Getting Started
To get started with QuizU, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/albertopuliga/QuizU.git
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Google API key:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Enable the [Generative AI API](https://console.cloud.google.com/marketplace/product/aiplatform/generative-ai-api)
   - Create a new API key and save it in a secure location (e.g., `.env` file)
   - Set the `GOOGLE_API_KEY` environment variable to the API key

4. Run the application:
   ```bash
   streamlit run src/app.py
   ```

## Usage
1. Upload your study materials (txt, pdf, docx files)
2. Enter your text directly
3. Select the number of questions to generate
4. Click "Generate Quiz" to generate the quiz questions
6. Click "Check Answer" to see if your answer is correct