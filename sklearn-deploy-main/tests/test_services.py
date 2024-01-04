import unittest
from api.utils.services import insert_user, read_user, update_user, \
    update_credit_score, fetch_credit_score # Replace with your actual module name

class MockCursor(object):
    def __init__(self) -> str:
        self.mocked_cache = {}
        self.return_value = None

    def execute(self, query, args):
        if (query, str(args)) in self.mocked_cache:
            self.return_value = self.mocked_cache[(query, str(args))]()
        else:
            raise KeyError

    def close(self):
        self.mocked_cache = {}

    def mock(self, query, args, fn):
        self.mocked_cache[(query, str(args))] = fn
    
    def fetchone(self):
        return self.return_value

class MockConnection(object):
    def __init__(self, *tables) -> None:
        self._cursor = MockCursor()
        for table in tables:
            self.stored_data = {table: {}}
    
    def cursor(self):
        return self._cursor
    
    def commit(self):
        pass

class TestInsertUser(unittest.TestCase):

    def setUp(self):
        self.query = "INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s)"
        self.mock_connection = MockConnection()
        self.mock_cursor = self.mock_connection.cursor()

    def test_successful_insertion(self):
        self.user_data = ["user1", 1.1, 1.1, 1.1, 1.1, 1.1]
        self.mock_cursor.mock(self.query, self.user_data, lambda: (_ for _ in ()))
        user_id, error = insert_user(self.mock_connection, self.user_data)
        self.assertEqual(user_id, 'user1')
        self.assertIsNone(error)

    def test_reinsert(self):
        self.user_data = ["user1", 1.1, 1.1, 1.1, 1.1, 1.1]
        self.mock_cursor.mock(self.query, self.user_data, lambda: (_ for _ in ()).throw(Exception("re insert")))
        user_id, error = insert_user(self.mock_connection, self.user_data)
        self.assertIsNone(user_id)
        self.assertIsNotNone(error)

    def test_insertion_with_connection_error(self):
        self.user_data = ["user1", 1.1, 1.1, 1.1, 1.1, 1.1]
        user_id, error = insert_user(self.mock_connection, self.user_data)
        self.assertIsNone(user_id)
        self.assertIsNotNone(error)

class TestReadUser(unittest.TestCase):

    def setUp(self):
        self.query = "SELECT * FROM users WHERE customer_id = %s"
        self.mock_connection = MockConnection()
        self.mock_cursor = self.mock_connection.cursor()

    def test_successful_read(self):
        self.user_data = ["user1", 1.1, 1.1, 1.1, 1.1, 1.1]
        customer_id = self.user_data[0]
        self.mock_cursor.mock(self.query, (customer_id,), lambda: self.user_data )
        returned_user = read_user(self.mock_connection, customer_id)
        self.assertEqual(self.user_data, returned_user)

    def test_read_no_record(self):
        self.mock_cursor.mock(self.query, ("user2",) , lambda: [])
        returned_user = read_user(self.mock_connection, "user2")
        self.assertEqual(returned_user, [])
    
    def test_wrong_query(self):
        returned_user = read_user(self.mock_connection, "user2")
        self.assertIsNone(returned_user)

class TestUpdateUser(unittest.TestCase):

    def setUp(self):
        self.query = """
            UPDATE users
            SET Credit_History_Age = %s,
                Monthly_Balance = %s,
                Annual_Income = %s,
                Changed_Credit_Limit = %s,
                Outstanding_Debt = %s
            WHERE customer_id = %s
        """
        self.mock_connection = MockConnection()
        self.mock_cursor = self.mock_connection.cursor()

    def test_successful_update(self):
        user_data = ["user1", 1.1, 1.1, 1.1, 1.1, 1.1]
        updated_data = ["user1", 1.2, 1.2, 1.2, 1.2, 1.2]
        customer_id = user_data[0]
        self.mock_cursor.mock(self.query, (1.2, 1.2, 1.2, 1.2, 1.2, "user1"), lambda: updated_data )
        returned_user = update_user(self.mock_connection, customer_id, [1.2, 1.2, 1.2, 1.2, 1.2])
        returned_user = self.mock_cursor.fetchone()
        self.assertEqual(updated_data, returned_user)
    
    def test_wrong_query(self):
        returned_user = read_user(self.mock_connection, "user2")
        self.assertIsNone(returned_user)

class TestUpdateCreditScore(unittest.TestCase):

    def setUp(self):
        self.query = """
            INSERT INTO creditscore
            VALUES (%s, %s, %s)
            ON CONFLICT (customer_id, model_key) DO UPDATE
            SET creditscore = EXCLUDED.creditscore
        """
        self.mock_connection = MockConnection()
        self.mock_cursor = self.mock_connection.cursor()

    def test_successful_insertion(self):
        credit_data= ["user1", "knn", "Good"]
        self.mock_cursor.mock(self.query, ("user1", "knn", "Good"), lambda: credit_data)
        update_credit_score(
            self.mock_connection, "user1", "knn", "Good")
        return_value = self.mock_cursor.fetchone()
        self.assertEqual(credit_data, return_value)
    
    def test_reinsert(self):
        credit_data= ["user1", "knn", "Bad"]
        self.mock_cursor.mock(self.query, ("user1", "knn", "Bad"), lambda: credit_data)
        update_credit_score(
            self.mock_connection, "user1", "knn", "Bad")
        return_value = self.mock_cursor.fetchone()
        self.assertEqual(credit_data, return_value)
    
    def test_new_key(self):
        credit_data= ["user1", "knn2", "Good"]
        self.mock_cursor.mock(self.query, ("user1", "knn2", "Good"), lambda: credit_data)
        update_credit_score(
            self.mock_connection, "user1", "knn2", "Good")
        return_value = self.mock_cursor.fetchone()
        self.assertEqual(credit_data, return_value)

class TestFetchCreditScore(unittest.TestCase):

    def setUp(self):
        self.query = "SELECT creditscore FROM creditscore WHERE customer_id = %s AND model_key = %s"
        self.mock_connection = MockConnection()
        self.mock_cursor = self.mock_connection.cursor()

    def test_successful_insertion(self):
        credit_data= ["user1", "knn", "Good"]
        self.mock_cursor.mock(self.query, ("user1", "knn"), lambda: ["Good"])
        score = fetch_credit_score(
            self.mock_connection, "user1", "knn")
        self.assertEqual(score, "Good")
    
    def test_reinsert(self):
        credit_data= ["user1", "knn", "Bad"]
        self.mock_cursor.mock(self.query, ("user1", "knn"), lambda: ["Bad"])
        score = fetch_credit_score(
            self.mock_connection, "user1", "knn")
        self.assertEqual(score, "Bad")
    
    def test_no_match(self):
        credit_data= ["user1", "knn2", "Good"]
        self.mock_cursor.mock(self.query, ("user1", "knn2"), lambda: None)
        score = fetch_credit_score(
            self.mock_connection, "user1", "knn")
        self.assertIsNone(score)


if __name__ == '__main__':
    unittest.main()
