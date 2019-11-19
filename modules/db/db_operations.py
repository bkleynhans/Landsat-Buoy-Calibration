###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Database operations module
# Created By          : Benjamin Kleynhans
# Creation Date       : August 10, 2018
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : August 15, 2019
# Filename            : db_operations.py
#
###

# Imports
from modules.db import db_connection
import pdb
import sys

class Db_Operations:
    
    #Class Attributes
    cursor = None
    
    
    # Initializer / Instance Attributes
    def __init__(self):
        self.cnx = db_connection.Db_Connection()
        
        
    # Build queries to be executed
    @staticmethod
    def query_builder(self, query_type, table, field, value, returnValue = None):
        
        query = None
        
        if query_type == 'exists':
                
            query = "SELECT COUNT(`{}`) FROM `{}` WHERE `{}` = '{}'".format(field, 
                                                                            table, 
                                                                            field, 
                                                                            value)
            
        elif query_type == 'insert':
            
            query = "INSERT INTO `{}`(`{}`) VALUES('{}')".format(table,
                                                                 field,
                                                                 value)
            
        elif query_type == 'select':
            
            query = "SELECT `{}` FROM `{}` WHERE `{}` = '{}'".format(returnValue,
                                                                     table,
                                                                     field,
                                                                     value)
                        
        return query
    
    
    # Checks if a value already exists in a table
    @staticmethod
    def value_exists(self, table, field, value):
        
        returnValue = False
        db_value = None
        
        query = self.query_builder(self, 'exists', table, field, value)
        
        try:
            cursor = self.cnx.open_connection()
            
            cursor.execute(query)
        
            db_value = cursor.fetchone()
            db_value = db_value[0]
        
        except Exception as e:
            print("\n Error occurred in db_operations.value_exists for table {}, field {}, value {}".format(table, field, value))
            print("\n {}".format(str(e)))
            
        finally:
            self.cnx.close_connection()
        
        if db_value != 0:
            returnValue = True
            
        return returnValue
    
    
    # Check if a row of data exists in the data table
    # Checks if a value already exists in a table
    @staticmethod
    def row_exists(self, scene_index, date_index, buoy_index):
        
        returnValue = False
        db_value = None
        
        query = "SELECT COUNT(`f_id`) FROM `t_data` WHERE " \
                "`f_scene_id` = '{}' AND " \
                "`f_date` = '{}' AND " \
                "`f_buoy_id` = '{}'".format(scene_index,
                                           date_index,
                                           buoy_index)
        
        try:
            cursor = self.cnx.open_connection()
            
            cursor.execute(query)
        
            db_value = cursor.fetchone()
            db_value = db_value[0]
        
        except Exception as e:
            print("\n Error occurred in db_operations.row_exists for scene index {}, date_index {}, buoy_index {}".format(scene_index, date_index, buoy_index))
            print("\n {}".format(str(e)))
            
        finally:
            self.cnx.close_connection()
        
        if db_value != 0:
            returnValue = True
            
        return returnValue
    
    
    # Format provided table name to have the correct format (just in case)
    @staticmethod
    def format_table_name(self, table_name):
        
        if table_name[0:2] != 't_':
            table_name = 't_' + table_name
        
        if table_name[-1:] != 's':
            table_name += 's'
            
        return table_name
    
    
    # Retrieve the index of a value from a table
    @staticmethod
    def get_index(self, table, value, value_field):
        
        returnValue = None
        
        index_field = 'f_id'
        
        try:
            query = self.query_builder(self, 'select', table, value_field, value, index_field)
            
            cursor = self.cnx.open_connection()
            
            cursor.execute(query)
            
            returnValue = cursor.fetchone()
            returnValue = returnValue[0]
            
        except Exception as e:
            print("\n Error occurred in db_operations.get_index for table {}, value {}, field, {}".format(table, value, value_field))
            print("\n {}".format(str(e)))
            
        finally:
            self.cnx.close_connection()
        
        return returnValue
        
    
    # Read a file into memory
    @staticmethod
    def read_image(self, scene_id):
        
        image = None
        
        image_file = 'output//processed_images//{}.tif'.format(scene_id)
        
        try:
            with open(image_file, 'rb') as image:
                image = image.read()
        except Exception as e:
            print("\n Error occurred in db_operations.read_image for Scene ID {}".format(scene_id))
            print("\n {}".format(str(e)))
        
        return image
    
    # Checks if an image already exists in the database
    @staticmethod
    def image_exists(self, scene_id):
        
        value_exists = None
        
        returnValue = False
        
        try:
            self.cursor = self.cnx.open_connection()
        
            query = "SELECT COUNT(`f_id`) FROM `t_images` WHERE `f_scene_id` = '{}'".format(scene_id)
            
            self.cursor.execute(query, scene_id)
            
            value_exists = self.cursor.fetchone()
            value_exists = value_exists[0]
            
        except Exception as e:
            print("\n Error occurred in db_operations.image_exists for Scene ID {}".format(scene_id))
            print("\n {}".format(str(e)))
            
        finally:
            self.cnx.close_connection()
        
        if value_exists != 0:
            returnValue = True
        
        return returnValue
    
    
    # Upload the default 'No Image' image
    def insert_image(self, scene_id):
        
        image_index = None
        
        insert_image = self.read_image(self, scene_id)
                
        # Convert image to tuple in order to insert
        insert_image = (insert_image,)
        
        #image_exists = self.image_exists(self, scene_id)
        image_exists = self.value_exists(self, 't_images', 'f_scene_id', scene_id)
        
        if not image_exists:        
            try:
                
                query = "INSERT INTO `t_images`(`f_scene_id`, `f_image`) VALUES('{}', %s)".format(scene_id)
                
                self.cursor = self.cnx.open_connection()
                self.cursor.execute(query, insert_image)
                self.cnx.db_commit()
                
                image_index = self.cursor.lastrowid
                    
            except Exception as e:
                print("\n Error occurred in db_operations.insert_image for Scene ID {}".format(scene_id))
                print("\n {}".format(str(e)))
                
            finally:
                self.cnx.close_connection()
                
        else:
            image_index = self.get_index(self, 't_images', scene_id, 'f_scene_id')
            
        return image_index
            

    # Insert a scene_id into the database and return its index
    def insert_single_value(self, table, value = None, scene_id = None):
        
        value_index = None
        
        if table == 't_dates':
            value = value.replace(hour=0, minute=0, second=0, microsecond=0)
        
        table = self.format_table_name(self, table)
        
        value_field ='f_' + table[2:-1]
        
        if table != 't_images':
            # Test if the scene id already exists in the database
            entry_exists = self.value_exists(self, table, value_field, value)
            
        else:
            entry_exists = self.image_exists(self, table, scene_id)
        
        # If it does not exist, insert it
        if not entry_exists:            
            try:
                query = self.query_builder(self, 'insert', table, value_field, value)
                
                cursor = self.cnx.open_connection()
                
                cursor.execute(query)
                
                self.cnx.db_commit()
                
                value_index = cursor.lastrowid
                
            except Exception as e:
                print("\n Error occurred in db_operations.insert_single_value into {}".format(table))
                print("\n {}".format(str(e)))
                
            finally:
                self.cnx.close_connection()
        
        else:
            value_index = self.get_index(self, table, value, value_field)
            
        return value_index
    
    
    # Insert a scene_id into the database and return its index
    def insert_data_row(self, scene_index, date_index, buoy_index, values, image_index, status, error_message):
        
        returnValue = None
        
        if date_index is None:
            date_index = 1
            
        if buoy_index is None:
            buoy_index = 1
        
        row_exists = self.row_exists(self, scene_index, date_index, buoy_index)
        
        if image_index == None:
            image_index = 1
        
        if not row_exists:
            try:
                query = "INSERT INTO `t_data`(`f_scene_id`, `f_date`, `f_buoy_id`, " \
                        "`f_bulk_temp`, `f_skin_temp`, `f_buoy_lat`, `f_buoy_lon`, " \
                        "`f_mod1`, `f_mod2`, `f_img1`, `f_img2`, `f_error1`, `f_error2`, " \
                        "`f_image`, `f_status`, `f_comment`) VALUES ( " \
                        "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, '{}', '{}' " \
                        ")".format(scene_index,
                                   date_index,
                                   buoy_index,
                                   values[0], # bulk_temp,
                                   values[1], # skin_temp,
                                   values[2], # buoy_lat,
                                   values[3], # buoy_lon,
                                   values[4][10], # mod_ltoa[10].value,
                                   values[4][11], # mod_ltoa[11].value,
                                   values[5][10], # img_ltoa[10].value,
                                   values[5][11], # img_ltoa[11].value,
                                   values[6][10], # error[10].value,
                                   values[6][11], # error[11].value,
                                   image_index,
                                   status,
                                   error_message)
                
                cursor = self.cnx.open_connection()
                
                cursor.execute(query)
                
                self.cnx.db_commit()
                
            except Exception as e:
                print("\n Error occurred in db_operations.insert_data_row scene index {}".format(scene_index))
                print("\n {}".format(str(e)))
                
            finally:
                self.cnx.close_connection()
                
        return returnValue
        