import os
from dataclasses import dataclass

from demo_web_app import demo_web_app
from gpt import GPT, Example
from gpt import set_openai_key
from ui_config import UIConfig


@dataclass
class Reaction:
    lhs: str
    rhs: str


combustion_reactions = [

    # Train
    Reaction("2H2+O2", "2H2O"),
    Reaction("C3H8+5O2", "3CO2+4H2O"),
    Reaction("CH4+2O2", "CO2+2H2O"),  # combustion of methane
    Reaction("C2H5OH+3O2", "2CO2+3H2O"),

    # Validation
    Reaction("C5H12+8O2", "5CO2+6H2O"),
    Reaction("2C2H6+7O2", "4CO2+6H2O"),  # combustion of ethane
    Reaction("2C4H10+13O2", "8CO2+10H2O"),  # combustion of butane
    Reaction("2C3H8+7O2", "6CO2+8H2O"),
    Reaction("CH10H4+12O2", "10CO2+4H2O"),  # burning of naphthalene
    Reaction("2C3H8+7O2", "6CO2+8H2O"),
]


def main():
    openai_key = os.getenv("OPENAI_KEY")
    set_openai_key(openai_key)
    gpt = GPT(temperature=0.2, max_tokens=10)

    train, validation = combustion_reactions[:4], combustion_reactions[4:]

    for example in train:
        gpt.add_example(Example(example.lhs, example.rhs))

    for idx, example in enumerate(validation):
        print(idx + 1)
        print(f"GPT prediction: {gpt.get_top_reply(example.lhs)}")
        print(f"Actual: {example.rhs}")
        print("==========================")

    # config = UIConfig(
    #     description="GPT-3 Alchemy", button_text="Predict Reaction", placeholder=""
    # )
    #
    # demo_web_app(gpt, openai_key, config)


if __name__ == "__main__":
    main()
