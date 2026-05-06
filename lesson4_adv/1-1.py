import sys
from typing import List, Optional, Union


class Token:
    """토큰 클래스 - 수식을 구성하는 기본 단위"""

    def __init__(self, _type: str, _value: str) -> None:
        self.type: str = _type  # 토큰 타입: 'NUMBER', 'OPERATOR', 'LPAREN', 'RPAREN'
        self.value: str = _value  # 토큰 값: '3', '+', '(', ')' 등

    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"


class TreeNode:
    """트리 노드 클래스 - 수식을 바이너리 트리로 표현"""

    def __init__(self, _value: str) -> None:
        self.value: str = _value  # 노드의 값 (숫자 또는 연산자)
        self.left: Optional["TreeNode"] = None  # 왼쪽 자식 노드
        self.right: Optional["TreeNode"] = None  # 오른쪽 자식 노드

    def is_operator(self) -> bool:
        # 1. self.value가 '+', '-', '*', '/' 중 하나이면 True, 아니면 False 반환

        return self.value in ["+", "-", "*", "/"]

    def is_number(self) -> bool:
        # 1. self.is_operator()가 False이면 True, 아니면 False 반환
        # (연산자가 아니면 숫자)

        return not self.is_operator()

    def __repr__(self) -> str:
        return f"Node({self.value})"


class Calculator:
    def __init__(self) -> None:
        self.tokens: List[Token] = []  # 토큰 리스트
        self.pos: int = 0  # 현재 파싱 위치

    def tokenize(self, _expression: str) -> List[Token]:
        # 수식을 토큰으로 분리
        # 예: "3 + 5 * 2" -> [Token(NUMBER, 3), Token(OPERATOR, +), Token(NUMBER, 5), ...]

        tokens: List[Token] = []
        i: int = 0

        while i < len(_expression):
            char = _expression[i]

            # 1. char가 공백(' ')이면:
            #    - i를 1 증가시키고 continue
            #
            # 2. char가 숫자('0'~'9') 또는 '.'이면:
            #    - number 변수를 빈 문자열("")로 초기화
            #    - while i < len(_expression) and (_expression[i].isdigit() or _expression[i] == '.'):
            #      * number에 _expression[i]를 추가 (number += _expression[i])
            #      * i를 1 증가
            #    - tokens에 Token('NUMBER', number)를 추가
            #    - continue
            #
            # 3. char가 '+'이거나 '-'이거나 '*'이거나 '/'이면:
            #    - tokens에 Token('OPERATOR', char)를 추가
            #    - i를 1 증가시키고 continue
            #
            # 4. char가 '('이면:
            #    - tokens에 Token('LPAREN', char)를 추가
            #    - i를 1 증가시키고 continue
            #
            # 5. char가 ')'이면:
            #    - tokens에 Token('RPAREN', char)를 추가
            #    - i를 1 증가시키고 continue
            #
            # 6. 그 외의 경우:
            #    - raise ValueError(f"잘못된 문자: {char}")

            i += 1

        return tokens

    def parse(self, _tokens: List[Token]) -> TreeNode:
        self.tokens = _tokens
        self.pos = 0

        return self._parse_expression()

    def _parse_expression(self) -> TreeNode:
        # 1. left 변수를 만들고, self._parse_term()을 저장
        #
        # 2. while self.pos < len(self.tokens):
        #    - token 변수를 self.tokens[self.pos]로 설정
        #    - token.type이 'OPERATOR'이고 token.value가 '+' 또는 '-'이면:
        #      * self.pos를 1 증가
        #      * operator_node 변수를 TreeNode(token.value)로 만들기
        #      * operator_node.left를 left로 설정
        #      * operator_node.right를 self._parse_term()으로 설정
        #      * left를 operator_node로 설정
        #    - 그렇지 않으면:
        #      * break
        #
        # 3. left를 반환

        return left

    def _parse_term(self) -> TreeNode:
        # 1. left 변수를 만들고, self._parse_factor()를 저장
        #
        # 2. while self.pos < len(self.tokens):
        #    - token 변수를 self.tokens[self.pos]로 설정
        #    - token.type이 'OPERATOR'이고 token.value가 '*' 또는 '/'이면:
        #      * self.pos를 1 증가
        #      * operator_node 변수를 TreeNode(token.value)로 만들기
        #      * operator_node.left를 left로 설정
        #      * operator_node.right를 self._parse_factor()로 설정
        #      * left를 operator_node로 설정
        #    - 그렇지 않으면:
        #      * break
        #
        # 3. left를 반환

        return left

    def _parse_factor(self) -> TreeNode:
        # 1. token 변수를 self.tokens[self.pos]로 설정
        #
        # 2. token.type이 'NUMBER'이면:
        #    - self.pos를 1 증가
        #    - TreeNode(token.value)를 반환
        #
        # 3. token.type이 'LPAREN'이면: (괄호 시작)
        #    - self.pos를 1 증가
        #    - node 변수를 self._parse_expression()으로 설정
        #    - self.tokens[self.pos].type이 'RPAREN'인지 확인
        #    - self.pos를 1 증가
        #    - node를 반환
        #
        # 4. 그 외의 경우:
        #    - raise ValueError(f"예상치 못한 토큰: {token}")

        return TreeNode("0")

    def evaluate(self, _node: Optional[TreeNode]) -> float:
        # 1. _node가 None이면, 0.0을 반환
        #
        # 2. _node.is_number()이면:
        #    - float(_node.value)를 반환
        #
        # 3. _node.is_operator()이면:
        #    - left_val 변수를 만들고, self.evaluate(_node.left)를 저장
        #    - right_val 변수를 만들고, self.evaluate(_node.right)를 저장
        #
        #    - _node.value가 '+'이면, left_val + right_val 반환
        #    - _node.value가 '-'이면, left_val - right_val 반환
        #    - _node.value가 '*'이면, left_val * right_val 반환
        #    - _node.value가 '/'이면:
        #      * right_val이 0이면, raise ValueError("0으로 나눌 수 없습니다.")
        #      * left_val / right_val 반환
        #
        # 4. 그 외의 경우:
        #    - raise ValueError(f"알 수 없는 연산자: {_node.value}")

        return 0.0

    def calculate(self, _expression: str) -> float:
        """수식을 입력받아 계산 결과 반환"""

        # 1. tokens 변수를 만들고, self.tokenize(_expression)를 저장
        # 2. tokens가 비어있으면, 0.0을 반환
        # 3. tree 변수를 만들고, self.parse(tokens)를 저장
        # 4. result 변수를 만들고, self.evaluate(tree)를 저장
        # 5. result를 반환

        return 0.0


if __name__ == "__main__":  # 이 파일 내에서만 실행됨!
    calc = Calculator()

    # 1. calc.calculate("3 + 5") 실행하고 결과를 출력
    # 2. calc.calculate("10 - 3") 실행하고 결과를 출력
