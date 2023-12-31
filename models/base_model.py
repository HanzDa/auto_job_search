from db_utils.database import Database


class HelperModel:
    def __init__(self):
        self.db = Database()

    def _get_child_attributes(self, ignore_pk=False):
        child_attributes = {}
        for key, value in dict(self.__getstate__()).items():
            if not value or key == 'db':
                continue
            child_attributes[key] = value

        # for security purposes
        if ignore_pk and 'pk' in child_attributes:
            child_attributes.pop('pk')

        return child_attributes

    @staticmethod
    def _get_clean_column_values(values):
        clean_values = []
        for value in values:
            if type(value) == str:
                value = value.replace("'", "`")

            clean_values.append(value)
        return tuple(clean_values)

    @staticmethod
    def _get_query_constraints(**constraints):
        query_constraints = ''
        for counter, (key, value) in enumerate(constraints.items(), start=1):
            query_constraints += f"{key} = '{value}'"
            if len(constraints) - counter > 0:
                query_constraints += ' AND '

        return query_constraints

    @staticmethod
    def fill_instance(instance, values_dict):
        for key, value in values_dict.items():
            instance.__setattr__(key, value)


class BaseModel(HelperModel):
    def __init__(self):
        super().__init__()

    # --------------- CRUD -----------------
    @staticmethod
    def update_instance(instance_id, **kwargs):
        pass

    @staticmethod
    def delete(instance_id, **kwargs):
        pass

    @classmethod
    def get(cls, fields=(), **kwargs):
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
        if row_dict:
            instance.fill_instance(instance, row_dict)
            instance.db.close_connection()
            return instance

    @classmethod
    def create(cls, **kwargs):
        """ Creates a new record in the database.
            returns: instance of calling class
        """
        instance = cls(**kwargs)
        child_attributes = instance._get_child_attributes(ignore_pk=True)  # pk is automatically added in db
        column_names = ", ".join(child_attributes.keys())
        column_values = instance._get_clean_column_values(child_attributes.values())
        query = f"""
                INSERT INTO {cls.Meta.table_name} 
                ({column_names}) VALUES {column_values}
                RETURNING pk
            """.replace('\n', '')
        is_ok = instance.db.execute_query(query)
        if is_ok:
            instance.pk = instance.db.cursor.fetchone()[0]
            instance.db.conn.commit()
            instance.db.close_connection()
            return instance

    @classmethod
    def get_all(cls, **kwargs):
        pass

    @classmethod
    def get_or_create(cls, fields=(), constraints={}, **kwargs):
        instance = cls.get(fields, **constraints) if constraints else None
        if not instance:
            instance = cls.create(**kwargs)

        return instance
