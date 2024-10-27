from datetime import datetime
from typing import Optional, Dict, Any, Union
from .base_model import BaseModel
from core.lib import db

class Transaction(BaseModel):
    def __init__(self, user_id: int, customer_id: int, paid_amount: float, voucher_id: Optional[int] = None):
        self.transaction_id: Optional[int] = None
        self.user_id = user_id
        self.customer_id = customer_id
        self.paid_amount = paid_amount
        self.voucher_id = voucher_id
        self.created_at = datetime.now()

    def create(self) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {
                "status": "error",
                "message": "Database connection error."
            }

        try:
            cursor.execute(
                '''INSERT INTO transactions (user_id, customer_id, paid_amount, voucher_id, created_at) 
                   VALUES (?, ?, ?, ?, ?)''', 
                (self.user_id, self.customer_id, self.paid_amount, self.voucher_id, self.created_at)
            )
            conn.commit()
            success = cursor.rowcount > 0
            transaction_id = cursor.lastrowid if success else None
            conn.close()

            response = {
                "status": "success" if success else "error",
                "message": f"Transaction saved successfully." if success else "Failed to save transaction."
            }
            if success:
                response["data"] = {"transaction_id": transaction_id}
            
            return response

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error creating transaction: {str(e)}"
            }

    def get_all(self) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {
                "status": "error",
                "message": "Database connection error."
            }

        try:
            cursor.execute('''
                SELECT t.*, u.username as cashier_name, c.phone as customer_phone
                FROM transactions t
                LEFT JOIN users u ON t.user_id = u.user_id
                LEFT JOIN customers c ON t.customer_id = c.customer_id
                ORDER BY t.transaction_id DESC
            ''')
            transactions = cursor.fetchall()
            conn.close()

            response = {
                "status": "success",
                "message": "Transactions retrieved successfully." if transactions else "No transactions found."
            }
            if transactions:
                response["data"] = transactions
            
            return response

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error retrieving transactions: {str(e)}"
            }

    def get_by_id(self, transaction_id: int) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {
                "status": "error",
                "message": "Database connection error."
            }

        try:
            cursor.execute('''
                SELECT t.*, u.username as cashier_name, c.phone as customer_phone
                FROM transactions t
                LEFT JOIN users u ON t.user_id = u.user_id
                LEFT JOIN customers c ON t.customer_id = c.customer_id
                WHERE t.transaction_id = ?
            ''', (transaction_id,))
            transaction = cursor.fetchone()
            conn.close()

            response = {
                "status": "success" if transaction else "error",
                "message": "Transaction retrieved successfully." if transaction else f"Transaction with ID {transaction_id} not found."
            }
            if transaction:
                response["data"] = transaction
            
            return response

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error retrieving transaction: {str(e)}"
            }

    def get_by_customer(self, customer_id: int) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {
                "status": "error",
                "message": "Database connection error."
            }

        try:
            cursor.execute('''
                SELECT t.*, u.username as cashier_name, c.phone as customer_phone
                FROM transactions t
                LEFT JOIN users u ON t.user_id = u.user_id
                LEFT JOIN customers c ON t.customer_id = c.customer_id
                WHERE t.customer_id = ?
                ORDER BY t.transaction_id DESC
            ''', (customer_id,))
            transactions = cursor.fetchall()
            conn.close()

            response = {
                "status": "success",
                "message": "Transactions retrieved successfully." if transactions else f"No transactions found for customer ID {customer_id}."
            }
            if transactions:
                response["data"] = transactions
            
            return response

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error retrieving transactions: {str(e)}"
            }

    def update(self) -> Dict[str, Union[str, Any]]:
        if self.transaction_id is None:
            return {
                "status": "error",
                "message": "Transaction ID is required to update a transaction."
            }

        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {
                "status": "error",
                "message": "Database connection error."
            }

        try:
            cursor.execute(
                '''UPDATE transactions SET paid_amount = ?, voucher_id = ? WHERE transaction_id = ?''',
                (self.paid_amount, self.voucher_id, self.transaction_id)
            )
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()

            return {
                "status": "success" if success else "error",
                "message": "Transaction updated successfully." if success else "Failed to update transaction or no changes were made."
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error updating transaction: {str(e)}"
            }

    def delete(self) -> Dict[str, Union[str, Any]]:
        if self.transaction_id is None:
            return {
                "status": "error",
                "message": "Transaction ID is required to delete a transaction."
            }

        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {
                "status": "error",
                "message": "Database connection error."
            }

        try:
            cursor.execute('''DELETE FROM transactions WHERE transaction_id = ?''', (self.transaction_id,))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()

            return {
                "status": "success" if success else "error",
                "message": f"Transaction with ID {self.transaction_id} deleted successfully." if success else f"Failed to delete transaction with ID {self.transaction_id} or transaction does not exist."
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error deleting transaction: {str(e)}"
            }

    def get_stats(self) -> Dict[str, Union[str, Any]]:
        conn, cursor = db.init_db()
        if conn is None or cursor is None:
            return {
                "status": "error",
                "message": "Database connection error."
            }

        try:
            cursor.execute('''
            SELECT 
                COUNT(CASE WHEN DATE(created_at) = DATE('now') THEN 1 END) AS daily_new_transactions,
                COUNT(CASE WHEN DATE(created_at) >= DATE('now', '-7 days') THEN 1 END) AS weekly_new_transactions,
                COUNT(CASE WHEN DATE(created_at) >= DATE('now', '-1 month') THEN 1 END) AS monthly_new_transactions
            FROM transactions;
            ''')
            stats = cursor.fetchone()
            conn.close()

            response = {
                "status": "success",
                "message": "Transaction statistics retrieved successfully."
            }
            if stats:
                response["data"] = {
                    "daily_new_transactions": stats[0],
                    "weekly_new_transactions": stats[1],
                    "monthly_new_transactions": stats[2],
                }
            
            return response

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error retrieving transaction statistics: {str(e)}"
            }