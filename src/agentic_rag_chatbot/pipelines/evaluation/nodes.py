from datasets import Dataset 
from ragas.metrics import faithfulness, answer_relevancy
from ragas import evaluate

from agentic_rag_chatbot.utils.config import set_secrets


set_secrets()


class RetrievalAugmentedGenerationEval():
    def __init__(self, faithfulness=False, answer_relevancy=False) -> None:
        self.faithfulness = faithfulness
        self.answer_relevancy = answer_relevancy

    @staticmethod
    def _parse_input_as_dataset(question: str, context: str, answer: str):

        data_sample = {
            'question': [question],
            'contexts' : [[context]],
            'answer': [answer],
        }

        dataset = Dataset.from_dict(data_sample)

        return dataset

    def _get_metric_functions(self):

        metrics = []

        if self.faithfulness:
            metrics.append(faithfulness)

        if self.answer_relevancy:
            metrics.append(answer_relevancy)

        return metrics

    def run(self, question: str, context: str, answer: str, report_level: str = "dataset"):

        dataset = self._parse_input_as_dataset(question, context, answer)
        metrics = self._get_metric_functions()

        eval_report = evaluate(dataset, metrics=metrics)

        if report_level == "dataset":
            return dict(eval_report)
        elif report_level == "item":
            return eval_report.to_pandas()
