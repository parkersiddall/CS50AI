from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(

    # A can be only a knight or a knave, not both
    Or(AKnave, AKnight), 

    # If A is a knight then he is not a knave
    Biconditional(AKnight, Not(AKnave)), 

    # If A is a knave then he is not a knight
    Biconditional(AKnave, Not(AKnight)), 

    # If he is a knight then it implies that he is both
    Implication(AKnight, And(AKnight, AKnave)),

    # if he is a knave then it implies that he is not both
    Implication(AKnave, Not(And(AKnave, AKnight)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(

    # It can be only a knight or a knave, not both
    Or(AKnave, AKnight), 
    Or(BKnight, BKnave),

    # If it is a knight then he is not a knave
    Biconditional(AKnight, Not(AKnave)), 
    Biconditional(BKnight, Not(BKnave)), 

    # If it is a knave then he is not a knight
    Biconditional(AKnave, Not(AKnight)), 
    Biconditional(BKnave, Not(BKnight)), 

    # if A is a knave then what they say is false
    Implication(AKnave, Not(And(AKnave, BKnave))),

    # if A is a knight then they really would be knaves
    Implication(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(

    # it can be only a knight or a knave, not both
    Or(AKnave, AKnight), 
    Or(BKnight, BKnave),

    # If it is a knight then he is not a knave
    Biconditional(AKnight, Not(AKnave)), 
    Biconditional(BKnight, Not(BKnave)), 

    # If it is a knave then he is not a knight
    Biconditional(AKnave, Not(AKnight)), 
    Biconditional(BKnave, Not(BKnight)), 

    # If A is a knight then both A and B are knights
    Implication(AKnight, And(AKnight, BKnight)),

    # If A is a Knave, then A and B are different and B must be a knight
    Implication(AKnave, BKnight), 

    # If B is a knight then A is a knave
    Implication(BKnight, AKnave), 

    # If B is a knave then both A and B are knaves
    Implication(BKnave, AKnave)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(

    # It can be only a knight or a knave, not both
    Or(AKnave, AKnight), 
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),

    # If it is a knight then he is not a knave
    Biconditional(AKnight, Not(AKnave)), 
    Biconditional(BKnight, Not(BKnave)), 
    Biconditional(CKnight, Not(CKnave)),

    # If it is a knave then he is not a knight
    Biconditional(AKnave, Not(AKnight)), 
    Biconditional(BKnave, Not(BKnight)), 
    Biconditional(CKnave, Not(CKnight)), 


    # If A is a knight then B is a knave and C is a knight
    Implication(AKnight, And(BKnave, CKnight)),

    # If B is a knave then A is not a knave and C is a knight
    Implication(BKnave, And(Not(AKnave), CKnight)), 

    # If C is a knight then A is a night and B is a knave
    Implication(CKnight, And(AKnight, BKnave)), 

    # If C is a knave then A is not a knight and B is a knight
    Implication(CKnave, And(Not(AKnight), BKnight)), 

    # If A is a knave then B is a knave, because there is no was a knave could say 'I am a knave'
    Implication(AKnave, BKnave)

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()



