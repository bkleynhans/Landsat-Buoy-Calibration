###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Database construction module
# Created By          : Benjamin Kleynhans
# Creation Date       : August 8, 2018
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : August 15, 2019
# Filename            : db_constructor.py
#
###

# Imports
from modules.db import db_connection
import pdb
import sys
import datetime

class Db_Construction:
    
    #Class Attributes
    cursor = None
    table_dictionary = {'t_scene_ids': False,
                        't_dates': False,
                        't_buoy_ids': False,
                        't_images': False,
                        't_data': False}
    
    generic_tables = {'t_scene_ids': False,
                      't_dates': False,
                      't_buoy_ids': False,
                      't_images': False}
    
    
    # Initializer / Instance Attributes
    def __init__(self):
        self.cnx = db_connection.Db_Connection()
    
    
    # Test if required tables exist in the database
    def database_ready(self):
        
        returnValue = True
        
        print(" Checking for required tables... \n")
        
        self.cursor = self.cnx.open_connection()
        
        query = "SHOW TABLES"
        
        self.cursor.execute(query)
        
        for table in self.cursor:
            if self.table_dictionary.__contains__(table[0].lower()):
                self.table_dictionary[table[0]] = True
                
        for table in self.table_dictionary:
            if not self.table_dictionary[table]:
                returnValue = False                
                break
        
        self.cnx.close_connection()
        
        return returnValue
    
    
    # Builds the query string to pass to SQL server
    @staticmethod
    def build_query(self, query_type, table_name, scene_id = None):
        
        query = None
        
        if query_type == 'create_table':
            if table_name in self.generic_tables:
                    
                data_type = None
                field_name = None
                    
                if table_name == 't_scene_ids':
                    data_type = "VARCHAR(40) NOT NULL"
                    field_name = "f_scene_id"
                    
                elif table_name == 't_dates':
                    data_type = "DATE NOT NULL"
                    field_name = "f_date"
                    
                elif table_name == 't_buoy_ids':
                    data_type = "MEDIUMINT NOT NULL"
                    field_name = "f_buoy_id"
                
                if table_name != 't_images':
                    query = "CREATE TABLE IF NOT EXISTS `{}` (" \
                            "`f_id` INT UNSIGNED NOT NULL AUTO_INCREMENT, " \
                            "`{}` {}, " \
                            "PRIMARY KEY(`f_id`), " \
                            "UNIQUE INDEX `f_id_UNIQUE` (`f_id` ASC), " \
                            "UNIQUE INDEX `{}_UNIQUE` (`{}` ASC) " \
                            ")ENGINE=InnoDB".format(table_name,
                                                    field_name,
                                                    data_type,
                                                    field_name,
                                                    field_name)
                else:
                    query = "CREATE TABLE IF NOT EXISTS `t_images` (" \
                            "`f_id` INT UNSIGNED NOT NULL AUTO_INCREMENT, " \
                            "`f_scene_id` VARCHAR(40) NOT NULL, " \
                            "`f_image` MEDIUMBLOB NOT NULL, " \
                            "PRIMARY KEY(`f_id`), " \
                            "UNIQUE INDEX `f_id_UNIQUE` (`f_id` ASC), " \
                            "UNIQUE INDEX `f_scene_id_UNIQUE` (`f_scene_id` ASC) " \
                            ")ENGINE=InnoDB"
                
            elif table_name == 't_data':
                
                query = "CREATE TABLE IF NOT EXISTS `t_data` (" \
                        "`f_id` INT UNSIGNED NOT NULL AUTO_INCREMENT," \
                        "`f_scene_id` INT UNSIGNED NOT NULL," \
                        "`f_date` INT UNSIGNED NOT NULL," \
                        "`f_buoy_id` INT UNSIGNED NOT NULL," \
                        "`f_bulk_temp` DOUBLE NULL," \
                        "`f_skin_temp` DOUBLE NULL," \
                        "`f_buoy_lat` FLOAT(6,3) NULL," \
                        "`f_buoy_lon` FLOAT(6,3) NULL," \
                        "`f_mod1` DOUBLE NULL," \
                        "`f_mod2` DOUBLE NULL," \
                        "`f_img1` DOUBLE NULL," \
                        "`f_img2` DOUBLE NULL," \
                        "`f_error1` DOUBLE NULL," \
                        "`f_error2` DOUBLE NULL," \
                        "`f_image` INT UNSIGNED NOT NULL DEFAULT 1," \
                        "`f_status` TEXT NULL," \
                        "`f_comment` TEXT NULL," \
                        "PRIMARY KEY(`f_id`)," \
                        "UNIQUE INDEX `f_id_UNIQUE` (`f_id` ASC)" \
                        ")ENGINE=InnoDB"
                
        elif query_type == 'create_triggers':
            if table_name == 't_data':
                
                query = "CREATE TRIGGER tg_data_insert BEFORE INSERT ON t_data " \
                        "FOR EACH ROW " \
                        "BEGIN " \
                        "SET NEW.f_scene_id = IFNULL(NEW.f_scene_id, '');" \
                        "SET NEW.f_date = IFNULL(NEW.f_date, 0);" \
                        "SET NEW.f_buoy_id = IFNULL(NEW.f_buoy_id, 0);" \
                        "SET NEW.f_bulk_temp = IFNULL(NEW.f_bulk_temp, 0);" \
                        "SET NEW.f_skin_temp = IFNULL(NEW.f_skin_temp, 0);" \
                        "SET NEW.f_buoy_lat = IFNULL(NEW.f_buoy_lat, 0);" \
                        "SET NEW.f_buoy_lon = IFNULL(NEW.f_buoy_lon, 0);" \
                        "SET NEW.f_mod1 = IFNULL(NEW.f_mod1, 0);" \
                        "SET NEW.f_mod2 = IFNULL(NEW.f_mod2, 0);" \
                        "SET NEW.f_img1 = IFNULL(NEW.f_img1, 0);" \
                        "SET NEW.f_img2 = IFNULL(NEW.f_img2, 0);" \
                        "SET NEW.f_error1 = IFNULL(NEW.f_error1, 0);" \
                        "SET NEW.f_error2 = IFNULL(NEW.f_error2, 0);" \
                        "SET NEW.f_image = IFNULL(NEW.f_image, 1);" \
                        "SET NEW.f_status = IFNULL(NEW.f_status, '');" \
                        "SET NEW.f_comment = IFNULL(NEW.f_comment, '');" \
                        "END;"
                
        elif query_type == 'create_indexes':
            if table_name in self.generic_tables:
                
                field_name = table_name[1:-2]
                
                query = "ALTER TABLE `{}` " \
                        "ADD INDEX `idx_{}_{}`(`{}` ASC);".format(table_name,
                                                                table_name,
                                                                field_name,
                                                                field_name)
                        
            elif table_name == 't_data':
                
                query = "ALTER TABLE `{}` " \
                        "ADD INDEX `idx_{}_f_id`(`f_id` ASC), " \
                        "ADD INDEX `idx_{}_f_scene_id`(`f_scene_id` ASC), " \
                        "ADD INDEX `idx_{}_f_date`(`f_date` ASC), " \
                        "ADD INDEX `idx_{}_f_buoy_id`(`f_buoy_id` ASC);".format(table_name,
                                                                                table_name,
                                                                                table_name,
                                                                                table_name,
                                                                                table_name)
                        
        elif query_type == 'add_constraints':
            if table_name == 't_data':

                query = "ALTER TABLE `{}` " \
                        "ADD CONSTRAINT `fk_t_scene_ids-{}` " \
                        "FOREIGN KEY (`f_id`) " \
                        "REFERENCES `{}` (`f_scene_id`) " \
                        "ON DELETE NO ACTION " \
                        "ON UPDATE CASCADE, " \
                        "ADD CONSTRAINT `fk_t_dates-{}` " \
                        "FOREIGN KEY (`f_id`) " \
                        "REFERENCES `{}` (`f_date`) " \
                        "ON DELETE NO ACTION " \
                        "ON UPDATE CASCADE, " \
                        "ADD CONSTRAINT `fk_t_buoy_ids-{}` " \
                        "FOREIGN KEY (`f_id`) " \
                        "REFERENCES `{}` (`f_buoy_id`) " \
                        "ON DELETE NO ACTION " \
                        "ON UPDATE CASCADE, " \
                        "ADD CONSTRAINT `fk_t_images-{}` " \
                        "FOREIGN KEY (`f_id`) " \
                        "REFERENCES `{}` (`f_image`) " \
                        "ON DELETE NO ACTION " \
                        "ON UPDATE CASCADE;".format(table_name,
                                                    table_name,
                                                    table_name,
                                                    table_name,
                                                    table_name,
                                                    table_name,
                                                    table_name,
                                                    table_name,
                                                    table_name)
                        
        elif query_type == 'create_view':
            if table_name == 'default_view':
                
                query = "CREATE VIEW `default_view` AS " \
                        "SELECT " \
                        "    `t_scene_ids`.`f_scene_id` AS 'Scene ID', " \
                        "    `t_dates`.`f_date` AS 'Date', " \
                        "    `t_buoy_ids`.`f_buoy_id` AS 'Buoy ID', " \
                        "    `t_data`.`f_bulk_temp` AS 'Bulk Temp', " \
                        "    `t_data`.`f_skin_temp` AS 'Skin Temp', " \
                        "    `t_data`.`f_buoy_lat` AS 'Buoy Lat', " \
                        "    `t_data`.`f_buoy_lon` AS 'Buoy Lon', " \
                        "    `t_data`.`f_mod1` AS 'Modelled B10', " \
                        "    `t_data`.`f_mod2` AS 'Modelled B11', " \
                        "    `t_data`.`f_img1` AS 'Landsat B10', " \
                        "    `t_data`.`f_img2` AS 'Landsat B11', " \
                        "    `t_data`.`f_error1` AS 'Error B10', " \
                        "    `t_data`.`f_error2` AS 'Error B11', " \
                        "    `t_images`.`f_image` AS 'Image', " \
                        "    `t_data`.`f_status` AS 'Status', " \
                        "    `t_data`.`f_comment` AS 'Comment' " \
                        "FROM " \
                        "    `t_data` " \
                        "        JOIN " \
                        "    `t_scene_ids` ON `t_scene_ids`.`f_id` = `t_data`.`f_scene_id` " \
                        "        JOIN " \
                        "    `t_dates` ON `t_dates`.`f_id` = `t_data`.`f_date` " \
                        "        JOIN " \
                        "    `t_buoy_ids` ON `t_buoy_ids`.`f_id` = `t_data`.`f_buoy_id` " \
                        "        JOIN " \
                        "    `t_images` ON `t_images`.`f_id` = `t_data`.`f_image`;"
                        
            if table_name == 'default_view_success':
                
                query = "CREATE VIEW `default_view_success` AS " \
                        "SELECT " \
                        "    `t_scene_ids`.`f_scene_id` AS 'Scene ID', " \
                        "    `t_dates`.`f_date` AS 'Date', " \
                        "    `t_buoy_ids`.`f_buoy_id` AS 'Buoy ID', " \
                        "    `t_data`.`f_bulk_temp` AS 'Bulk Temp', " \
                        "    `t_data`.`f_skin_temp` AS 'Skin Temp', " \
                        "    `t_data`.`f_buoy_lat` AS 'Buoy Lat', " \
                        "    `t_data`.`f_buoy_lon` AS 'Buoy Lon', " \
                        "    `t_data`.`f_mod1` AS 'Modelled B10', " \
                        "    `t_data`.`f_mod2` AS 'Modelled B11', " \
                        "    `t_data`.`f_img1` AS 'Landsat B10', " \
                        "    `t_data`.`f_img2` AS 'Landsat B11', " \
                        "    (`t_data`.`f_mod1` - `t_data`.`f_img1`) AS 'Diff B10', " \
                        "    (`t_data`.`f_mod2` - `t_data`.`f_img2`) AS 'Diff B11', " \
                        "    `t_data`.`f_error1` AS 'Error B10', " \
                        "    `t_data`.`f_error2` AS 'Error B11', " \
                        "    `t_images`.`f_image` AS 'Image', " \
                        "    `t_data`.`f_status` AS 'Status', " \
                        "    `t_data`.`f_comment` AS 'Comment' " \
                        "FROM " \
                        "    `t_data` " \
                        "        JOIN " \
                        "    `t_scene_ids` ON `t_scene_ids`.`f_id` = `t_data`.`f_scene_id` " \
                        "        JOIN " \
                        "    `t_dates` ON `t_dates`.`f_id` = `t_data`.`f_date` " \
                        "        JOIN " \
                        "    `t_buoy_ids` ON `t_buoy_ids`.`f_id` = `t_data`.`f_buoy_id` " \
                        "        JOIN " \
                        "    `t_images` ON `t_images`.`f_id` = `t_data`.`f_image` " \
                        "WHERE " \
                        "    `t_data`.`f_status` = 'success';"
                        
            if table_name == 'default_view_failure':
                
                query = "CREATE VIEW `default_view_failure` AS " \
                        "SELECT " \
                        "    `t_scene_ids`.`f_scene_id` AS 'Scene ID', " \
                        "    `t_dates`.`f_date` AS 'Date', " \
                        "    `t_buoy_ids`.`f_buoy_id` AS 'Buoy ID', " \
                        "    `t_data`.`f_bulk_temp` AS 'Bulk Temp', " \
                        "    `t_data`.`f_skin_temp` AS 'Skin Temp', " \
                        "    `t_data`.`f_buoy_lat` AS 'Buoy Lat', " \
                        "    `t_data`.`f_buoy_lon` AS 'Buoy Lon', " \
                        "    `t_data`.`f_mod1` AS 'Modelled B10', " \
                        "    `t_data`.`f_mod2` AS 'Modelled B11', " \
                        "    `t_data`.`f_img1` AS 'Landsat B10', " \
                        "    `t_data`.`f_img2` AS 'Landsat B11', " \
                        "    `t_data`.`f_error1` AS 'Error B10', " \
                        "    `t_data`.`f_error2` AS 'Error B11', " \
                        "    `t_images`.`f_image` AS 'Image', " \
                        "    `t_data`.`f_status` AS 'Status', " \
                        "    `t_data`.`f_comment` AS 'Comment' " \
                        "FROM " \
                        "    `t_data` " \
                        "        JOIN " \
                        "    `t_scene_ids` ON `t_scene_ids`.`f_id` = `t_data`.`f_scene_id` " \
                        "        JOIN " \
                        "    `t_dates` ON `t_dates`.`f_id` = `t_data`.`f_date` " \
                        "        JOIN " \
                        "    `t_buoy_ids` ON `t_buoy_ids`.`f_id` = `t_data`.`f_buoy_id` " \
                        "        JOIN " \
                        "    `t_images` ON `t_images`.`f_id` = `t_data`.`f_image` " \
                        "WHERE " \
                        "    `t_data`.`f_status` = 'failed';"
        
        return query
    
    
    # Passes query string to SQL server.
    @staticmethod
    def create_table(self, query, table_name):
        
        print("\n Creating table {}.".format(table_name))
        
        try:
            self.cursor = self.cnx.open_connection()
            
            self.cursor.execute(query)
            self.cnx.db_commit()
            
            self.cnx.close_connection()
        except:
            print("Exception occurred during table creation")
        
        print("\n The table {} has been created".format(table_name))
        
    
    # Create database triggers
    @staticmethod
    def create_triggers(self):
        
        print("\n Creating triggers for table t_data.")
        
        try:
            self.cursor = self.cnx.open_connection()
            
            query = self.build_query(self, 'create_triggers', 'data')
            
            self.cursor.execute(query)
            self.cnx.db_commit()
            
        except:
            print("Exception occurred during trigger creation")
            
        finally:
            self.cnx.close_connection()
            
        print("\n Triggers for t_data have been created")
        
        
    # Create default view
    @staticmethod
    def create_default_views(self):
        
        view_list = ['default_view', 'default_view_success', 'default_view_failure']
        
        print("\n Create default database views")
        
        for view in view_list:        
            try:
                self.cursor = self.cnx.open_connection()
                
                query = self.build_query(self, 'create_view', view)
                
                self.cursor.execute(query)
                self.cnx.db_commit()
                
            except:
                print("Exception occurred during default view creation")
                
            finally:
                self.cnx.close_connection()            
            
        print("\n Default views created")

    
    # Update database indexes
    @staticmethod
    def add_indexes(self):
            
        try:            
            self.cursor = self.cnx.open_connection()
        
            for table in self.table_dictionary:
                
                print("\n Adding indices for {}.".format(table))
                
                table = table[2:]
                
                query = self.build_query(self, 'create_indexes', table)
                
                self.cursor.execute(query)
                self.cnx.db_commit()
                
                print("\n Indices for {} have been added".format(table))
                
        except:
            print("Exception occurred during index creation for table {}".format(table))
            
        finally:
            self.cnx.close_connection()
                
    
    # Add table constraints
    @staticmethod
    def add_constraints(self):
        
        constraint_list = {'index', 
                           'dictionary'}

        try:            
            self.cursor = self.cnx.open_connection()
     
            for table in constraint_list:
                
                print("\n Adding constraints for {}.".format(table))
                
                query = self.build_query(self, 'add_constraints', table)
                
                self.cursor.execute(query)
                self.cnx.db_commit()
                
                print("\n Constraints for {} have been added".format(table))
                
        except:
            print("Exception occurred during constraint creation for table {}".format(table))
            
        finally:
            self.cnx.close_connection()
       

    # Read a file into memory
    @staticmethod
    def read_no_image(self):
        
        no_image = None
        
        default_image_file = 'tools//no_image.tif'
        
        try:
            with open(default_image_file, 'rb') as default_image:
                no_image = default_image.read()
        except:
            print("\n Error while reading default image file")
        
        return no_image
    

    # Load default values for data that doesn't exist
    @staticmethod
    def load_default_values(self):
        
        print("\n Loading default values.")
                
        default_value_tables = ['t_buoy_ids', 't_dates']
        default_table_values = {'t_buoy_ids': 0, 't_dates': datetime.datetime(1,1,1,0,0)}
        
        for table in default_value_tables:
            try:
                query = "INSERT INTO `{}`(`{}`) VALUES('{}')".format(table, "f_" + table[2:-1], default_table_values[table])
                
                self.cursor = self.cnx.open_connection()
                self.cursor.execute(query)
                self.cnx.db_commit()
                    
            except:
                print("Exception occurred during default value insertion.")
                
            finally:
                self.cnx.close_connection()                
        
        print("\n Default values added")


    # Upload the default 'No Image' image
    @staticmethod
    def upload_default_image(self):
        
        print("\n Adding default image.")
        
        no_image = self.read_no_image(self)
        
        # Convert image to tuple in order to insert
        no_image = (no_image,)
        
        try:   
            query = "INSERT INTO `t_images`(`f_scene_id`, `f_image`) VALUES('None', %s)"
            
            self.cursor = self.cnx.open_connection()
            self.cursor.execute(query, no_image)
            self.cnx.db_commit()
            
            print("\n Default image added")
                
        except:
            print("Exception occurred during default image upload.")
            
        finally:
            self.cnx.close_connection()
        
    
    # Prepare the database if it is not ready
    def prepare_database(self):
        
        query = None
        
        if not self.database_ready():
            
            sys.stdout.write("\n Some tables are missing from the database. "
                             " If you choose to create these tables, some data may "
                             " be lost.  Please make a backup of the database before "
                             " you continue.\n")
            
            please_continue = None
            
            while please_continue == None:
                please_continue = input("\n Do you want to continue to create the tables? (Y/N) : ").upper()
            
                if please_continue == 'Y':
                    please_continue = True
                elif please_continue == "N":
                    please_continue = False
                else:
                    print(" Your entry was invalid.")
                    please_continue = None
            
            if please_continue:            
                for table in self.table_dictionary:
                    
                    to_create = None
                    
                    if not self.table_dictionary[table]:
                        to_create = table
                        
                        query = self.build_query(self, 'create_table', table)
                    
                    if to_create != None:
                        self.create_table(self, query, to_create)
                    
                    query = None
                
                self.create_triggers(self)
                self.add_indexes(self)
                self.add_constraints(self)
                self.load_default_values(self)
                self.upload_default_image(self)
                self.create_default_views(self)
        