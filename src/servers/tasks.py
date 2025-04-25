from typing import List, Any
from fastmcp import FastMCP
from src.utils.database import NewDatabaseConnection
from src.utils.logger import logging

logs = logging
conn = NewDatabaseConnection()._connection()
tasks = FastMCP(
    name="tasks",
    instructions="The server provides tasks creation as create_task(), deletion as delete_task(), updation as update_task(), get active tasks as get_tasks() tools"
)

@tasks.tool()
def create_task(task_name: str | Any, remarks: str | Any = ""):
    """
        Info:
            The tool is used to create a new task
        Parameters:
         - task_name: str | Any = mandatory string field i.e task name to create a new task
         - remarks: str | Any = non mandatory string field i.e remarks if any
        Note:
         - conn is not a input paramter strict input task_name and remarks but don't use conn as input
    """
    try:
        cur = conn.cursor()
        insert_query = """
            INSERT INTO tasks(task_name, remarks)
            VALUES (%s, %s);
        """
        cur.execute(insert_query, (task_name, remarks))
        conn.commit()
        cur.close()
        logging.info("Task created successfully!")
        return {"status": "success", "message": "Task created successfully"}
        
    except Exception as err:
        logging.error(f"Error occurred while inserting new task: {err}")
        conn.rollback()
        return {"status": "error", "message": f"Failed to create task: {err}"}
    
@tasks.tool()
def get_tasks():
    """
        Info:
            The tool is used when users want to get list of all active tasks
    """

    result = []
    try:
        cur = conn.cursor()
        select_query = "SELECT id, task_name, remarks, created_at FROM tasks WHERE active = true;"
        cur.execute(select_query)
        output = cur.fetchall()
        cur.close()
        return output
    except Exception as err:
        logging.error(f"Error occurred while getting all active tasks: {err}")
        conn.rollback()
        return result

@tasks.tool()
def update_task(task_id: int, task_name: str | Any = None, remarks: str | Any = None):
    """
        Info:
            The tool is used to update an existing task
        Parameters:
         - task_id: int = mandatory integer field i.e task id to update
         - task_name: str | Any = optional string field to update task name
         - remarks: str | Any = optional string field to update remarks
    """
    try:
        cur = conn.cursor()
        update_parts = []
        values = []
        
        if task_name is not None:
            update_parts.append("task_name = %s")
            values.append(task_name)
            
        if remarks is not None:
            update_parts.append("remarks = %s")
            values.append(remarks)
            
        if not update_parts:
            return {"status": "error", "message": "No update parameters provided"}
            
        update_query = f"""
            UPDATE tasks
            SET {", ".join(update_parts)}
            WHERE id = %s AND active = true;
        """
        values.append(task_id)
        
        cur.execute(update_query, tuple(values))
        conn.commit()
        
        if cur.rowcount == 0:
            cur.close()
            return {"status": "error", "message": "No task found with the given ID or task is not active"}
            
        cur.close()
        logging.info(f"Task {task_id} updated successfully!")
        return {"status": "success", "message": f"Task {task_id} updated successfully"}
        
    except Exception as err:
        logging.error(f"Error occurred while updating task: {err}")
        conn.rollback()
        return {"status": "error", "message": f"Failed to update task: {err}"}

@tasks.tool()
def delete_task(task_id: int):
    """
        Info:
            The tool is used to delete (deactivate) a task
        Parameters:
         - task_id: int = mandatory integer field i.e task id to delete
    """
    try:
        cur = conn.cursor()
        delete_query = """
            UPDATE tasks
            SET active = false
            WHERE id = %s AND active = true;
        """
        cur.execute(delete_query, (task_id,))
        conn.commit()
        
        if cur.rowcount == 0:
            cur.close()
            return {"status": "error", "message": "No task found with the given ID or task is already inactive"}
            
        cur.close()
        logging.info(f"Task {task_id} deleted successfully!")
        return {"status": "success", "message": f"Task {task_id} deleted successfully"}
        
    except Exception as err:
        logging.error(f"Error occurred while deleting task: {err}")
        conn.rollback()
        return {"status": "error", "message": f"Failed to delete task: {err}"}
