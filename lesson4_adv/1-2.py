import sys
from typing import List, Optional, Union


class Token:
    """토큰 클래스 - 수식을 구성하는 기본 단위"""

    def __init__(self, _type: str, _value: str) -> None:
        self.type: str = _type
        self.value: str = _value

    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"


class TreeNode:
    """트리 노드 클래스 - 수식을 바이너리 트리로 표현"""

    def __init__(self, _value: str) -> None:
        self.value: str = _value
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None

    def is_operator(self) -> bool:
        """이 노드가 연산자인지 확인"""
        return self.value in ["+", "-", "*", "/"]

    def is_number(self) -> bool:
        """이 노드가 숫자인지 확인"""
        return not self.is_operator()

    def __repr__(self) -> str:
        return f"Node({self.value})"


class Calculator:
    def __init__(self) -> None:
        self.tokens: List[Token] = []
        self.pos: int = 0

    def tokenize(self, _expression: str) -> List[Token]:
        """수식을 토큰으로 분리, 예: "3 + 5 * 2" -> [Token(NUMBER, 3), Token(OPERATOR, +), Token(NUMBER, 5), ...]"""
        tokens: List[Token] = []
        i: int = 0

        while i < len(_expression):
            char = _expression[i]

            if char == " ":
                i += 1

                continue

            if char.isdigit() or char == ".":
                number = ""

                while i < len(_expression) and (_expression[i].isdigit() or _expression[i] == "."):
                    number += _expression[i]
                    i += 1

                tokens.append(Token("NUMBER", number))

                continue

            if char in ["+", "-", "*", "/"]:
                tokens.append(Token("OPERATOR", char))
                i += 1

                continue

            if char == "(":
                tokens.append(Token("LPAREN", char))
                i += 1

                continue

            if char == ")":
                tokens.append(Token("RPAREN", char))
                i += 1

                continue

            raise ValueError(f"잘못된 문자: {char}")

        return tokens

    def parse(self, _tokens: List[Token]) -> TreeNode:
        """토큰을 바이너리 트리로 변환, 연산자 우선순위를 고려하여 파싱"""
        self.tokens = _tokens
        self.pos = 0
        return self._parse_expression()

    def _parse_expression(self) -> TreeNode:
        """덧셈과 뺄셈을 처리 (가장 낮은 우선순위)"""
        left = self._parse_term()

        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]

            if token.type == "OPERATOR" and token.value in ["+", "-"]:
                self.pos += 1
                operator_node = TreeNode(token.value)
                operator_node.left = left
                operator_node.right = self._parse_term()
                left = operator_node
            else:
                break

        return left

    def _parse_term(self) -> TreeNode:
        """곱셈과 나눗셈을 처리 (중간 우선순위)"""
        left = self._parse_factor()

        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]

            if token.type == "OPERATOR" and token.value in ["*", "/"]:
                self.pos += 1
                operator_node = TreeNode(token.value)
                operator_node.left = left
                operator_node.right = self._parse_factor()
                left = operator_node
            else:
                break

        return left

    def _parse_factor(self) -> TreeNode:
        """숫자와 괄호를 처리 (가장 높은 우선순위)"""
        token = self.tokens[self.pos]

        if token.type == "NUMBER":
            self.pos += 1
            return TreeNode(token.value)

        if token.type == "LPAREN":
            self.pos += 1
            node = self._parse_expression()

            if self.tokens[self.pos].type != "RPAREN":
                raise ValueError("닫는 괄호가 없습니다.")

            self.pos += 1
            return node

        raise ValueError(f"예상치 못한 토큰: {token}")

    def evaluate(self, _node: Optional[TreeNode]) -> float:
        """트리를 순회하며 계산, 재귀적으로 왼쪽과 오른쪽 자식을 먼저 계산한 후, 현재 노드의 연산 수행"""
        if _node is None:
            return 0.0

        if _node.is_number():
            return float(_node.value)

        if _node.is_operator():
            left_val = self.evaluate(_node.left)
            right_val = self.evaluate(_node.right)

            if _node.value == "+":
                return left_val + right_val
            elif _node.value == "-":
                return left_val - right_val
            elif _node.value == "*":
                return left_val * right_val
            elif _node.value == "/":
                if right_val == 0:
                    raise ValueError("0으로 나눌 수 없습니다.")
                return left_val / right_val

        raise ValueError(f"알 수 없는 연산자: {_node.value}")

    def calculate(self, _expression: str) -> float:
        tokens = self.tokenize(_expression)

        if not tokens:
            return 0.0

        tree = self.parse(tokens)
        result = self.evaluate(tree)

        return result


if __name__ == "__main__":
    calc = Calculator()

    print("=== 식 계산기 ===")
    print("수식을 입력하세요. (종료: 'quit' 또는 'exit')")

    while True:
        try:
            expression = input("수식 입력 > ").strip()

            if expression.lower() in ["quit", "exit", "q"]:
                print("계산기를 종료합니다.")

                break

            if not expression:
                continue

            result = calc.calculate(expression)

            print(f"결과: {result}")
            print()

        except ValueError as e:
            print(f"오류: {e}")
            print()
        except IndexError:
            print("오류: 잘못된 수식 형식입니다.")
            print()
        except Exception as e:
            print(f"오류: {e}")
            print()
