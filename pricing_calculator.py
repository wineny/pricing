#!/usr/bin/env python3
"""
맞춤형 워크샵 견적 계산기
2일차/4일차 프로그램 가격 자동 계산
"""

from typing import Dict, Tuple
from dataclasses import dataclass


@dataclass
class PricingConfig:
    """가격 설정 (모든 금액은 원 단위)"""

    # 시간당 단가
    LECTURE_RATE = 750_000  # 강의 단가
    COACHING_RATE = 300_000  # 코칭/발표/진행 단가
    ASSISTANT_RATE = 300_000  # 보조강사 단가

    # 2일차 프로그램 시간
    DAY2_LECTURE_HOURS = 8  # 강의 시간
    DAY2_PRESENTATION_HOURS = 5  # 발표/진행 시간
    DAY2_COACHING_PER_PERSON = 1  # 1인당 코칭 시간

    # 4일차 프로그램 시간
    DAY4_LECTURE_HOURS = 11  # 강의 시간
    DAY4_PRESENTATION_HOURS = 6  # 발표/진행 시간
    DAY4_COACHING_HOURS = 11  # 상주 코칭 시간

    # 세일즈 최적화 단가 (구간별)
    SALES_DAY2_TIER1 = 1_000_000  # 10-20명 인당 단가
    SALES_DAY2_TIER2 = 900_000    # 21-30명 인당 단가
    SALES_DAY4_TIER1 = 1_400_000  # 10-20명 인당 단가
    SALES_DAY4_TIER2 = 1_200_000  # 21-30명 인당 단가


class WorkshopPricingCalculator:
    """워크샵 견적 계산기"""

    def __init__(self, config: PricingConfig = None):
        self.config = config or PricingConfig()

    @staticmethod
    def get_assistant_count(participants: int) -> int:
        """인원에 따른 보조강사 수 계산"""
        if participants <= 10:
            return 0
        elif participants <= 20:
            return 1
        else:  # 21-30명
            return 2

    def calculate_day2_original(self, participants: int) -> Dict[str, int]:
        """2일차 프로그램 원가 계산 (원본 로직)"""
        if not 1 <= participants <= 30:
            raise ValueError("인원은 1-30명 사이여야 합니다.")

        # 기본 비용 (메인 강사)
        lecture_cost = self.config.DAY2_LECTURE_HOURS * self.config.LECTURE_RATE
        presentation_cost = self.config.DAY2_PRESENTATION_HOURS * self.config.COACHING_RATE
        base_cost = lecture_cost + presentation_cost

        # 개별 코칭 비용
        coaching_cost = participants * self.config.DAY2_COACHING_PER_PERSON * self.config.COACHING_RATE

        # 보조강사 비용
        assistant_count = self.get_assistant_count(participants)
        assistant_hours = self.config.DAY2_LECTURE_HOURS + self.config.DAY2_PRESENTATION_HOURS
        assistant_cost = assistant_count * assistant_hours * self.config.ASSISTANT_RATE

        # 총액
        total = base_cost + coaching_cost + assistant_cost

        return {
            '기본비용': base_cost,
            '강의료': lecture_cost,
            '발표진행료': presentation_cost,
            '개별코칭료': coaching_cost,
            '보조강사수': assistant_count,
            '보조강사비': assistant_cost,
            '총액': total,
            '인당단가': total // participants
        }

    def calculate_day4_original(self, participants: int) -> Dict[str, int]:
        """4일차 프로그램 원가 계산 (원본 로직)"""
        if not 1 <= participants <= 30:
            raise ValueError("인원은 1-30명 사이여야 합니다.")

        # 기본 비용 (메인 강사)
        lecture_cost = self.config.DAY4_LECTURE_HOURS * self.config.LECTURE_RATE
        presentation_cost = self.config.DAY4_PRESENTATION_HOURS * self.config.COACHING_RATE
        coaching_cost = self.config.DAY4_COACHING_HOURS * self.config.COACHING_RATE
        base_cost = lecture_cost + presentation_cost + coaching_cost

        # 보조강사 비용
        assistant_count = self.get_assistant_count(participants)
        assistant_hours = (self.config.DAY4_LECTURE_HOURS +
                          self.config.DAY4_PRESENTATION_HOURS +
                          self.config.DAY4_COACHING_HOURS)
        assistant_cost = assistant_count * assistant_hours * self.config.ASSISTANT_RATE

        # 총액
        total = base_cost + assistant_cost

        return {
            '기본비용': base_cost,
            '강의료': lecture_cost,
            '발표진행료': presentation_cost,
            '상주코칭료': coaching_cost,
            '보조강사수': assistant_count,
            '보조강사비': assistant_cost,
            '총액': total,
            '인당단가': total // participants
        }

    def calculate_day2_sales(self, participants: int) -> Dict[str, int]:
        """2일차 프로그램 세일즈 가격 계산 (단순 구간 단가제)"""
        if not 1 <= participants <= 30:
            raise ValueError("인원은 1-30명 사이여야 합니다.")

        # 1-10명: 기본 + 개별 코칭
        if participants <= 10:
            base_cost = 7_500_000
            coaching_cost = participants * 300_000
            total = base_cost + coaching_cost
            per_person = total // participants
            tier = '1-10명 (기본 + 개별코칭)'
        # 11-20명: 구간 단가
        elif participants <= 20:
            per_person = self.config.SALES_DAY2_TIER1
            total = participants * per_person
            tier = '11-20명'
        # 21-30명: 구간 단가
        else:
            per_person = self.config.SALES_DAY2_TIER2
            total = participants * per_person
            tier = '21-30명'

        return {
            '인당단가': per_person,
            '총액': total,
            '적용구간': tier,
            '보조강사수': self.get_assistant_count(participants)
        }

    def calculate_day4_sales(self, participants: int) -> Dict[str, int]:
        """4일차 프로그램 세일즈 가격 계산 (단순 구간 단가제)"""
        if not 1 <= participants <= 30:
            raise ValueError("인원은 1-30명 사이여야 합니다.")

        # 1-10명: 고정 가격
        if participants <= 10:
            total = 13_350_000
            per_person = total // participants
            tier = '1-10명 (고정)'
        # 11-20명: 구간 단가
        elif participants <= 20:
            per_person = self.config.SALES_DAY4_TIER1
            total = participants * per_person
            tier = '11-20명'
        # 21-30명: 구간 단가
        else:
            per_person = self.config.SALES_DAY4_TIER2
            total = participants * per_person
            tier = '21-30명'

        return {
            '인당단가': per_person,
            '총액': total,
            '적용구간': tier,
            '보조강사수': self.get_assistant_count(participants)
        }

    def compare_programs(self, participants: int, use_sales_pricing: bool = True) -> Dict:
        """2일차 vs 4일차 프로그램 비교"""
        if use_sales_pricing:
            day2 = self.calculate_day2_sales(participants)
            day4 = self.calculate_day4_sales(participants)
        else:
            day2 = self.calculate_day2_original(participants)
            day4 = self.calculate_day4_original(participants)

        return {
            '인원': participants,
            '2일차': day2,
            '4일차': day4,
            '프로그램차액': day4['총액'] - day2['총액'],
            '인당차액': day4['인당단가'] - day2['인당단가']
        }

    def generate_price_table(self, use_sales_pricing: bool = True) -> str:
        """전체 가격표 생성 (텍스트 형식)"""
        participants_list = [5, 10, 11, 15, 20, 21, 25, 30]

        lines = []
        lines.append("=" * 100)
        lines.append("맞춤형 워크샵 견적표")
        lines.append("=" * 100)
        lines.append("")

        pricing_type = "세일즈 최적화 가격" if use_sales_pricing else "원가 기반 가격"
        lines.append(f"[{pricing_type}]")
        lines.append("")

        # 헤더
        lines.append(f"{'인원':<6} | {'2일차 총액':>15} | {'2일차 인당':>15} | {'4일차 총액':>15} | {'4일차 인당':>15} | {'차액':>15}")
        lines.append("-" * 100)

        # 데이터
        for n in participants_list:
            comparison = self.compare_programs(n, use_sales_pricing)
            day2_total = comparison['2일차']['총액']
            day2_per = comparison['2일차']['인당단가']
            day4_total = comparison['4일차']['총액']
            day4_per = comparison['4일차']['인당단가']
            diff = comparison['프로그램차액']

            lines.append(
                f"{n:>4}명 | {day2_total:>13,}원 | {day2_per:>13,}원 | "
                f"{day4_total:>13,}원 | {day4_per:>13,}원 | {diff:>13,}원"
            )

        lines.append("=" * 100)
        return "\n".join(lines)


def main():
    """대화형 견적 계산기"""
    calculator = WorkshopPricingCalculator()

    print("\n" + "=" * 60)
    print("맞춤형 워크샵 견적 계산기")
    print("=" * 60)

    while True:
        print("\n[메뉴]")
        print("1. 견적 계산 (세일즈 가격)")
        print("2. 견적 계산 (원가 기반)")
        print("3. 전체 가격표 보기 (세일즈)")
        print("4. 전체 가격표 보기 (원가)")
        print("5. 프로그램 비교")
        print("0. 종료")

        choice = input("\n선택: ").strip()

        if choice == '0':
            print("\n계산기를 종료합니다.")
            break

        elif choice in ['1', '2', '5']:
            try:
                participants = int(input("\n예상 인원 (1-30명): ").strip())

                if participants > 30:
                    print("\n" + "=" * 60)
                    print("🤝 별도 상담이 필요합니다")
                    print("=" * 60)
                    print("\n31명 이상의 대규모 교육은 맞춤형 견적이 필요합니다.")
                    print("담당자에게 문의해주세요.")
                    print("\n📧 이메일: contact@example.com")
                    print("📞 전화: 02-1234-5678\n")
                    continue

                if not 1 <= participants <= 30:
                    print("⚠️  인원은 1-30명 사이여야 합니다.")
                    continue

                use_sales = choice == '1'

                if choice == '5':
                    # 프로그램 비교
                    comparison = calculator.compare_programs(participants, use_sales)

                    print("\n" + "=" * 60)
                    print(f"프로그램 비교 ({participants}명 기준)")
                    print("=" * 60)
                    print(f"\n[2일차 프로그램]")
                    print(f"  총액: {comparison['2일차']['총액']:,}원")
                    print(f"  인당: {comparison['2일차']['인당단가']:,}원")
                    print(f"  보조강사: {comparison['2일차']['보조강사수']}명")

                    print(f"\n[4일차 프로그램]")
                    print(f"  총액: {comparison['4일차']['총액']:,}원")
                    print(f"  인당: {comparison['4일차']['인당단가']:,}원")
                    print(f"  보조강사: {comparison['4일차']['보조강사수']}명")

                    print(f"\n[차액 분석]")
                    print(f"  총액 차이: {comparison['프로그램차액']:,}원")
                    print(f"  인당 차이: {comparison['인당차액']:,}원")

                else:
                    # 프로그램 선택
                    print("\n[프로그램 선택]")
                    print("1. 2일차 프로그램")
                    print("2. 4일차 프로그램")
                    program = input("선택: ").strip()

                    if program == '1':
                        if use_sales:
                            result = calculator.calculate_day2_sales(participants)
                            print("\n" + "=" * 60)
                            print(f"2일차 프로그램 견적 (세일즈 가격)")
                        else:
                            result = calculator.calculate_day2_original(participants)
                            print("\n" + "=" * 60)
                            print(f"2일차 프로그램 견적 (원가 기반)")
                    elif program == '2':
                        if use_sales:
                            result = calculator.calculate_day4_sales(participants)
                            print("\n" + "=" * 60)
                            print(f"4일차 프로그램 견적 (세일즈 가격)")
                        else:
                            result = calculator.calculate_day4_original(participants)
                            print("\n" + "=" * 60)
                            print(f"4일차 프로그램 견적 (원가 기반)")
                    else:
                        print("⚠️  잘못된 선택입니다.")
                        continue

                    print("=" * 60)
                    print(f"\n참여 인원: {participants}명")
                    for key, value in result.items():
                        if isinstance(value, int) and key != '보조강사수':
                            print(f"{key}: {value:,}원")
                        else:
                            print(f"{key}: {value}")

            except ValueError as e:
                print(f"⚠️  오류: {e}")

        elif choice in ['3', '4']:
            use_sales = choice == '3'
            print("\n" + calculator.generate_price_table(use_sales))

        else:
            print("⚠️  잘못된 선택입니다.")


if __name__ == "__main__":
    main()
