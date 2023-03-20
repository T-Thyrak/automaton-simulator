import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from fa import FA

def test_from() -> None:
    fa_string = """{"states": ["q0", "q1", "q2"], "alphabet": ["a", "b"], "starting_state": "q0", "final_states": ["q2"], "transition_function": [{"from_state": "q0", "with_symbol": "a", "to_state": ["q1", "q2"]}, {"from_state": "q0", "with_symbol": "b", "to_state": ["q1"]}, {"from_state": "q1", "with_symbol": "a", "to_state": ["q2"]}, {"from_state": "q1", "with_symbol": "\u03b5", "to_state": ["q2"]}]}"""
        
    fa = FA.json_deserialize(fa_string)
    
    print(fa)
    
def test_minimize() -> None:
    fa_string = """{
        "states": ["q0", "q1", "q2", "q3"],
        "alphabet": ["0", "1"],
        "starting_state": "q0",
        "final_states": ["q2"],
        "transition_function": [
            {
                "from_state": "q2",
                "with_symbol": "1",
                "to_state": ["q3"]
            },
            {
                "from_state": "q2",
                "with_symbol": "0",
                "to_state": ["q3"]
            },
            {
                "from_state": "q3",
                "with_symbol": "1",
                "to_state": ["q3"]
            },
            {
                "from_state": "q3",
                "with_symbol": "0",
                "to_state": ["q3"]
            },
            {
                "from_state": "q0",
                "with_symbol": "1",
                "to_state": ["q3"]
            },
            {
                "from_state": "q0",
                "with_symbol": "0",
                "to_state": ["q1"]
            },
            {
                "from_state": "q1",
                "with_symbol": "1",
                "to_state": ["q3"]
            },
            {
                "from_state": "q1",
                "with_symbol": "0",
                "to_state": ["q2"]
            }
        ]
    }
    """
    
    fa = FA.json_deserialize(fa_string)
    print(fa)
    
    min_fa = fa.minimize()
    
    print(min_fa)
    
def test_minimize2():
    # 0 a -> 1
    # 0 b -> 5
    # 1 a -> 6
    # 1 b -> 2
    # 2 a -> 0
    # 2 b -> 2
    # 3 a -> 2
    # 3 b -> 6
    # 4 a -> 7
    # 4 b -> 5
    # 5 a -> 2
    # 5 b -> 6
    # 6 a -> 6
    # 6 b -> 4
    # 7 a -> 6
    # 7 b -> 2
    fa_string = """{
        "states": ["q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7"],
        "alphabet": ["a", "b"],
        "starting_state": "q0",
        "final_states": ["q2"],
        "transition_function": [
            {
                "from_state": "q0",
                "with_symbol": "a",
                "to_state": ["q1"]
            },
            {
                "from_state": "q0",
                "with_symbol": "b",
                "to_state": ["q5"]
            },
            {
                "from_state": "q1",
                "with_symbol": "a",
                "to_state": ["q6"]
            },
            {
                "from_state": "q1",
                "with_symbol": "b",
                "to_state": ["q2"]
            },
            {
                "from_state": "q2",
                "with_symbol": "a",
                "to_state": ["q0"]
            },
            {
                "from_state": "q2",
                "with_symbol": "b",
                "to_state": ["q2"]
            },
            {
                "from_state": "q3",
                "with_symbol": "a",
                "to_state": ["q2"]
            },
            {
                "from_state": "q3",
                "with_symbol": "b",
                "to_state": ["q6"]
            },
            {
                "from_state": "q4",
                "with_symbol": "a",
                "to_state": ["q7"]
            },
            {
                "from_state": "q4",
                "with_symbol": "b",
                "to_state": ["q5"]
            },
            {
                "from_state": "q5",
                "with_symbol": "a",
                "to_state": ["q2"]
            },
            {
                "from_state": "q5",
                "with_symbol": "b",
                "to_state": ["q6"]
            },
            {
                "from_state": "q6",
                "with_symbol": "a",
                "to_state": ["q6"]
            },
            {
                "from_state": "q6",
                "with_symbol": "b",
                "to_state": ["q4"]
            },
            {
                "from_state": "q7",
                "with_symbol": "a",
                "to_state": ["q6"]
            },
            {
                "from_state": "q7",
                "with_symbol": "b",
                "to_state": ["q2"]
            }
        ]
    }"""
    
    fa = FA.json_deserialize(fa_string)
    
    print(fa)
    
    min_fa = fa.minimize()
    
    print(min_fa)

def test_determinization():
    # 0 a -> 0
    # 0 b -> 0, 1
    # 1 a -> 2
    # 1 b -> 2
    # 1 eps -> 2
    # 2 a -> 3
    # 2 b -> 3
    # 3 final
    
    fa_string = """{
        "states": ["q0", "q1", "q2", "q3"],
        "alphabet": ["a", "b"],
        "starting_state": "q0",
        "final_states": ["q3"],
        "transition_function": [
            {
                "from_state": "q0",
                "with_symbol": "a",
                "to_state": ["q0"]
            },
            {
                "from_state": "q0",
                "with_symbol": "b",
                "to_state": ["q0", "q1"]
            },
            {
                "from_state": "q1",
                "with_symbol": "a",
                "to_state": ["q2"]
            },
            {
                "from_state": "q1",
                "with_symbol": "b",
                "to_state": ["q2"]
            },
            {
                "from_state": "q1",
                "with_symbol": "\u03B5",
                "to_state": ["q2"]
            },
            {
                "from_state": "q2",
                "with_symbol": "a",
                "to_state": ["q3"]
            },
            {
                "from_state": "q2", 
                "with_symbol": "b",
                "to_state": ["q3"] 
            }
        ]
    }"""
    
    fa = FA.json_deserialize(fa_string)
    
    det_fa = fa.determinize()
    
    print(det_fa.unwrap().json_serialize())

if __name__ == "__main__":
    test_determinization()
    pass