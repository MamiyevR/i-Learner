from openai import OpenAI
from dotenv import load_dotenv
from .prompts import Prompts
import app.db.schemas as schemas

load_dotenv()


class AIProvider:
    def __init__(self):
        # Initialize OpenAI client with GPT-4.1 model
        self.client = OpenAI()
        self.model = "gpt-4.1"
        # Map of supported AI tasks to their handler methods
        self.task_handlers = {
            "essay": self._handle_essay_generation,
            "mcq": self._handle_mcq_generation,
            "grade_essay": self._handle_essay_grading,
            "grade_mcq": self._handle_mcq_grading,
            "chat": self._handle_chat,
            "summarize": self._handle_summarize,
        }

    def execute(self, task: str, data: dict) -> dict:
        """
        Main public method to execute AI tasks.
        Args:
            task (str): The type of task to execute
            data (dict): The data required for the task
        Returns:
            dict: The result of the task execution
        """
        handler = self.task_handlers.get(task)
        if not handler:
            raise ValueError(f"Unknown task: {task}")
        return handler(data)

    def _create_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        structured_output=None,
    ) -> str | dict:
        """
        Helper method to create chat completions
        Args:
            system_prompt (str): The system prompt to guide the AI
            user_prompt (str): The user's input or content to process
            structured_output (dict | None): JSON schema for structured output.
                Example: {
                    "type": "object",
                    "properties": {
                        "score": {"type": "number"},
                        "feedback": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["score", "feedback"]
                }
        Returns:
            str | dict: String response or structured JSON object if schema provided
        """
        try:
            if structured_output:
                system_prompt += "\nYou must respond with a JSON object that matches the specified schema."

                response = self.client.beta.chat.completions.parse(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    response_format=structured_output,
                )

                result = response.choices[0].message.parsed
                if result:
                    result = result.dict()
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                )
                result = response.choices[0].message.content

            if result is None:
                return self._get_dummy_response(user_prompt)

            return result
        except Exception as e:
            print(f"Error in AI completion: {e}")
            return self._get_dummy_response(user_prompt)

    def _handle_essay_generation(self, data: dict) -> dict:
        """
        Handles essay generation task
        """
        result = self._create_completion(
            Prompts.ESSAY_SYSTEM,
            f"""Generate an essay prompt and expected answer based on the following content:\n\n{data.get('content', '')}""",
            structured_output=schemas.EssayContent,
        )

        if isinstance(result, dict):
            return result

        return {
            "prompt": "Failed to generate essay prompt",
            "expected_answer": "No answer generated",
        }

    def _handle_mcq_generation(self, data: dict) -> dict:
        """
        Handles MCQ generation task
        """
        result = self._create_completion(
            Prompts.MCQ_SYSTEM,
            f"""Generate 20 multiple choice questions based on the following content:\n\n{data.get('content', '')}""",
            structured_output=schemas.MCQContent,
        )

        if isinstance(result, dict):
            return result
        return {"questions": []}

    def _handle_essay_grading(self, data: dict) -> dict:
        """
        Handles essay grading task
        """
        system_prompt = Prompts.GRADE_ESSAY_SYSTEM.format(
            prompt=data.get("prompt", ""),
            content=data.get("content", ""),
            expected_answer=data.get("expected_answer", ""),
        )

        result = self._create_completion(
            system_prompt=system_prompt,
            user_prompt=f"""Grade this essay:\n\n{data.get('essay', '')}""",
            structured_output=schemas.EssayGradingResponse,
        )

        if isinstance(result, dict):
            return result
        return {"score": 0, "feedback": ["Failed to grade essay properly"]}

    def _handle_mcq_grading(self, data: dict) -> dict:
        """
        Handles MCQ grading task
        """
        system_prompt = Prompts.GRADE_MCQ_SYSTEM.format(
            questions=data.get("questions", []),
            correct_answers=data.get("correct_answers", []),
        )

        result = self._create_completion(
            system_prompt=system_prompt,
            user_prompt=f"""Grade these answers:\n\n{data.get('user_answers', [])}""",
            structured_output=schemas.MCQGradingResponse,
        )

        if isinstance(result, dict):
            return result

        return {"feedback": []}

    def _handle_chat(self, data: dict) -> dict:
        """
        Handles chat/tutoring task
        """
        system_prompt = Prompts.CHAT_SYSTEM.format(
            content=data.get("content", ""),
            assessment=data.get("assessment", {}),
        )

        if not data.get("message"):
            return {"response": "Please provide a message to chat with the AI."}

        return {
            "response": self._create_completion(system_prompt, data.get("message", ""))
        }

    def _handle_summarize(self, data: dict) -> dict:
        """
        Handles summarization task
        """

        result = self._create_completion(
            system_prompt=Prompts.SUMMARY_SYSTEM,
            user_prompt=f"""Summarize the following content:\n\n{data.get('content', '')}""",
            structured_output=schemas.SummaryResponse,
        )

        if isinstance(result, dict):
            return result

        return {
            "summary": "",
            "keyword": "",
        }

    def _get_dummy_response(self, prompt: str) -> str:
        """
        Provides dummy responses for testing or when API fails
        """
        return f"Dummy response for: {prompt}"
