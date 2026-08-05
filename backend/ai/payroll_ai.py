from sqlalchemy.orm import Session

from backend.models.payroll import Payroll


class PayrollAI:

    def get_payroll_summary(self, db: Session, employee_id: int):

        payroll = (
            db.query(Payroll)
            .filter(Payroll.employee_id == employee_id)
            .order_by(Payroll.pay_date.desc())
            .first()
        )

        if payroll is None:
            return None

        return {
            "basic_salary": payroll.basic_salary,
            "bonus": payroll.bonus,
            "allowances": payroll.allowances,
            "deductions": payroll.deductions,
            "net_salary": payroll.net_salary,
            "pay_date": str(payroll.pay_date)
        }


payroll_ai = PayrollAI()