from search import search_prompt
from dotenv import load_dotenv

load_dotenv()


def main():
    question_in_context_1 = "Qual o faturamento da Empresa SuperTechIABrazil?"
    question_without_context_1 = "Qual a localização da empresa SuperTechIABrazil?"

    print("Question One:\n")
    print(question_in_context_1)
    print(search_prompt(question_in_context_1))
    print("="*50)
    print("\nQuestion Two:\n")
    print(question_without_context_1)
    print(search_prompt(question_without_context_1))
    print("="*50)

if __name__ == "__main__":
    main()
