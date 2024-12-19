import os
import sys
import psycopg2
from typing import List
from fastapi import HTTPException
from model.Task import Task

class TaskController:

    @classmethod
    async def get_all_task(cls):
        tasks: List[Task] = []
        conn = cls._get_db_connection()
        if conn is Exception :
          raise HTTPException(status_code=500, detail=conn)
        with conn as connection:
            cur = connection.cursor()
            cur.execute("SELECT * FROM tasks")
            for row in cur.fetchall():
                tasks.append(Task.from_list(row))
        return tasks
            
    
    @classmethod
    async def get_task_by_id(cls, task_id: int):
        conn = cls._get_db_connection()
        if conn is Exception :
          raise HTTPException(status_code=500, detail=conn)
        with conn as connection:
            cur = connection.cursor()
            cur.execute(f"SELECT * FROM tasks WHERE id={task_id}")
            row = cur.fetchone()
        if row:
            return Task.from_list(row)
        else:
            raise HTTPException(status_code=404, detail="Task not found")

    @classmethod
    async def add_task(cls, task: Task):
        query = "INSERT INTO tasks (title, description, done) VALUES (%s, %s, %s)"
        conn = cls._get_db_connection()
        if conn is Exception :
          raise HTTPException(status_code=500, detail=conn)
        try: 
            with conn as connection:
                cur = connection.cursor()
                cur.execute(query=query, vars=tuple(vars(task).values())[1:])
                connection.commit()
            return task 
        except Exception as err:
            raise HTTPException(status_code=500, detail=err)
    
    @classmethod
    async def update_task(cls, task: Task):
        query = "UPDATE tasks SET title=%s, description=%s, done=%s WHERE id=%s"
        conn = cls._get_db_connection()
        if conn is Exception :
          raise HTTPException(status_code=500, detail=conn)
        try: 
            with conn as connection:
                cur = connection.cursor()
                cur.execute(query=query, vars=(task.title, task.description, task.done, task.id))
                connection.commit()
            return task 
        except Exception as err:
            raise HTTPException(status_code=500, detail=err)
    
    @classmethod
    async def delete_task(cls, task_id: int):
        conn = cls._get_db_connection()
        if conn is Exception :
          raise HTTPException(status_code=500, detail=conn)
        try: 
            with conn as connection:
                cur = connection.cursor()
                cur.execute(query=f"DELETE FROM tasks WHERE id={task_id}")
                connection.commit()
            return {"message": "Task deleted successfully"} 
        except Exception as err:
            raise HTTPException(status_code=500, detail=err)
    
    def _get_db_connection():
        host = os.getenv('DB_HOST')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        database =  os.getenv('DB')
        port = int(os.getenv('DB_PORT'))
        conn_str = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        try:
            conn = psycopg2.connect(conn_str)
            cur = conn.cursor()
            cur.execute(
                """CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                done BOOLEAN NOT NULL)
            """)
            return conn
        except Exception as err:
            print(err)
            return err