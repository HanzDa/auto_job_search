from dbutils.database import Database


class BaseModel:
    def __init__(self):
        self.db = Database()

    def _get_child_attributes(self, ignore_pk=False):
        child_attributes = {}
        for key, value in dict(self.__getstate__()).items():
            if value is None or key == 'db':
                continue
            child_attributes[key] = value

        if ignore_pk and 'pk' in child_attributes:
            child_attributes.pop('pk')

        return child_attributes

    @staticmethod
    def _get_query_constraints(**constraints):
        query_constraints = ''
        counter = 0
        for key, value in constraints.items():
            counter += 1
            query_constraints += f"{key} = '{value}'"
            if len(constraints) - counter > 0:
                query_constraints += ' AND '

        return query_constraints

    @staticmethod
    def fill_instance(instance, values_dict):
        for key, value in values_dict.items():
            instance.__setattr__(key, value)

    # --------------- CRUD -----------------
    @staticmethod
    def update_company(id, **kwargs):
        pass

    @staticmethod
    def delete_company(id, **kwargs):
        pass

    @classmethod
    def get_object(cls, fields=(), **kwargs):
        instance = cls()
        fields = ', '.join(fields) if fields else '*'
        constrain_fields = instance._get_query_constraints(**kwargs)

        query = f"""
            SELECT {fields} FROM {cls.Meta.table_name}
            WHERE {constrain_fields}
        """.replace('\n', '')

        instance.db.execute_query(query)
        row = instance.db.cursor.fetchone()
        column_names = [desc[0] for desc in instance.db.cursor.description] if fields != '*' else fields
        row_dict = dict(zip(column_names, row)) if row else {}
        instance.fill_instance(instance, row_dict)
        instance.db.close_connection()
        return instance

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        child_attributes = instance._get_child_attributes(ignore_pk=True)  # pk is automatically added in db
        column_names = ", ".join(child_attributes.keys())
        column_values = tuple(child_attributes.values())
        query = f"""
                INSERT INTO {cls.Meta.table_name} 
                ({column_names}) VALUES {column_values}
                RETURNING pk
            """.replace('\n', '')
        instance.db.execute_query(query)
        instance.pk = instance.db.cursor.fetchone()[0]
        instance.db.conn.commit()
        instance.db.close_connection()
        return instance

    @classmethod
    def get_objects(cls, **kwargs):
        pass
