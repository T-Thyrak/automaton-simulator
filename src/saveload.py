from fa import FA
from result import Result
from ext.sqlq import *
from ext.anything import dequote

def go_save(fa: FA, uid: int, fa_id: int | None) -> Result[int, str]:
    """Save the FA to the database."""
    db_conn = create_connection()
    
    if db_conn is None:
        return Result.Err("Could not connect to database.")
    
    # Check if the FA has already been saved
    query = "SELECT `fa_id` FROM farecord WHERE `fa_id` = %s AND `uid` = %s"
    
    res = execute_query(query, db_conn, (fa_id, uid))
    
    if res is None:
        return Result.Err("Could not find previously saved FA.")
    
    if len(res) == 0 or fa_id is None:
        # The FA has not been saved yet
        # Insert the FA
        query = "INSERT INTO `fatbl` (`fa_string`) VALUES (\"%s\")"
        # start_commit(db_conn)
        
        res = execute_query(query, db_conn, (fa.json_serialize(indent=None),))
        
        if res is None:
            # rollback(db_conn)
            return Result.Err("Could not insert FA into database.")
        
        # Get the ID of the FA
        fa_id = res
        
        # Insert the record
        query = "INSERT INTO `farecord` (`uid`, `fa_id`) VALUES (%s, %s)"
        
        res = execute_query(query, db_conn, (uid, fa_id))
        
        if res is None:
            # rollback(db_conn)
            return Result.Err("Could not insert FA record into database.")
        
        end_commit(db_conn)
        
        return Result.Ok(fa_id)
    else:
        # The FA has been saved before
        # Update the FA
        query = "UPDATE `fatbl` SET `fa_string` = \"%s\" WHERE `id` = %s"
        # start_commit(db_conn)
        
        res = execute_query(query, db_conn, (fa.json_deserialize(indent=None), fa_id))
        
        if res is None:
            # rollback(db_conn)
            return Result.Err("Could not update FA in database.")

        end_commit(db_conn)
        
        return Result.Ok(fa_id)

def go_save_new(fa: FA, uid: int) -> Result[int, str]:
    """Save the FA to the database without checking if it has been saved before."""
    db_conn = create_connection()
    
    if db_conn is None:
        return Result.Err("Could not connect to database.")
    
    # Insert the FA
    query = "INSERT INTO `fatbl` (`fa_string`) VALUES (\"%s\")"
    
    res = execute_query(query, db_conn, (fa.json_serialize(indent=None),))
    
    if res is None:
        return Result.Err("Could not insert FA into database.")
    
    # Get the ID of the FA
    fa_id = res
    
    # Insert the record
    query = "INSERT INTO `farecord` (`uid`, `fa_id`) VALUES (%s, %s)"
    
    res = execute_query(query, db_conn, (uid, fa_id))
    
    if res is None:
        return Result.Err("Could not insert FA record into database.")
    
    return Result.Ok(fa_id)
    
def go_load(uid: int, fa_id: int) -> Result[FA, str]:
    """Load the FA from the database."""
    
    db_conn = create_connection()
    
    if db_conn is None:
        return Result.Err("Could not connect to database.")
    
    # Verify that the user has the FA
    query = "SELECT `fa_id` FROM `farecord` WHERE `uid` = %s AND `fa_id` = %s"
    
    res = execute_query(query, db_conn, (uid, fa_id))
    
    if res is None:
        return Result.Err("Could not find previously saved FA.")
    
    if len(res) == 0:
        return Result.Err("Could not find previously saved FA.")
    
    # Check if the FA has already been saved
    query = "SELECT `fa_string` FROM `fatbl` WHERE `id` = %s"
    
    res = execute_query(query, db_conn, (fa_id,))
    
    if res is None:
        return Result.Err("Could not find previously saved FA.")
    
    if len(res) == 0:
        return Result.Err("Could not find previously saved FA.")
    
    fa_string = dequote(res[0][0])
    
    return Result.Ok(FA.json_deserialize(fa_string))
    
def show_saved_fa(uid: int) -> Result[list[int], str]:
    """Show the saved FA of the user."""
    
    query = "SELECT `fa_id` FROM `farecord` WHERE `uid` = %s"
    
    db_conn = create_connection()
    res = execute_query(query, db_conn, (uid,))
    
    if res is None:
        return Result.Err("Could not find previously saved FA.")
    
    return Result.Ok(list(map(lambda x: x[0], res)))

def is_valid_id(uid: int, fa_id: int) -> Result[bool, str]:
    """Check if the FA ID is valid."""
    
    query = "SELECT `fa_id` FROM `farecord` WHERE `uid` = %s AND `fa_id` = %s"
    
    db_conn = create_connection()
    res = execute_query(query, db_conn, (uid, fa_id))
    
    if res is None:
        return Result.Err("Could not find previously saved FA.")
    
    return Result.Ok(len(res) > 0)