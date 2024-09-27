"""
RAG Evaluation Pipeline

This pipeline evaluates the answer for a given question and (retrieved) context.
"""

from agentic_rag_chatbot.pipelines.evaluation.nodes import RetrievalAugmentedGenerationEval
from agentic_rag_chatbot.utils.config import get_params
from agentic_rag_chatbot.utils.logging import logger


params = get_params()
params_eval = params['evaluation']
eval_metrics = params_eval['metrics']


#rag_evaluator = RetrievalAugmentedGenerationEval(**eval_metrics)


answer_evaluator = RetrievalAugmentedGenerationEval(faithfulness=True, answer_relevancy=True)


def assess_rag_answer(question: str, context: str, answer: str) -> str:
    """
    Useful to determine whether a RAG-based answer is both relevant and factually accurate.

    The evaluation is based on two key metrics:

    - Answer Relevance: This metric measures how well the generated answer addresses the user's original question. 
      It evaluates the pertinence of the answer based on the question, context, and answer.

    - Answer Faithfulness: This metric assesses the factual accuracy of the answer in relation to the provided context. 
      A faithful answer is one in which all claims can be directly inferred from the context.

    Both metrics range from 0 to 1, where higher scores indicate better performance.

    Parameters:
        question (str): The user's original question.
        context (str): The relevant content from the retrieved information used to generate the answer.
        answer (str): The generated answer to be evaluated.

    Returns:
        dict: A dictionary wiht the scores for each metric.
    """

    assessment_report = answer_evaluator.run(question, context, answer)

    logger.info(f'Evaluates the generated RAG-based answer:\n{str(assessment_report)}')

    return assessment_report

if __name__ == "__main__":
    #Example

    import json

    question = 'When was the first super bowl?'
    context = 'The First AFL-NFL World Championship Game was an American football game played on January 15, 1967, at the Los Angeles Memorial Coliseum in Los Angeles'
    answer = 'The first superbowl was held on Jan 15, 1967'

    eval_report = assess_rag_answer(question, context, answer) 

    output = {"question": question, "context": context, "answer": answer, "evaluation report": eval_report}

    print(json.dumps(output, indent=4))
