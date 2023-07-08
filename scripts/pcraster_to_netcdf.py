#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

import pcraster as pcr

# utility modules:
import virtualOS as vos
import outputNetcdf as out_nc

def convert_pcraster_to_netcdf(\
                               input_pcr_map_file,\
                               output_netcdf_file,\
                               variable_name = None,\
                               netcdf_global_attributes = None,\
                               netcdf_y_orientation_from_top_bottom = True,\
                               variable_unit = "unknown",\
                               netcdf_format = "NETCDF4",\
                               netcdf_zlib_option = False,\
                               time_input = None,\
                               ):
    
    # read the pcraster map
    pcr.setclone(input_pcr_map_file)
    input_pcr_map = pcr.readmap(input_pcr_map_file)
    
    if variable_name is None: 
        variable_name = os.path.basename(input_pcr_map_file)

        # Note variable, dimension and attribute names should begin with a letter and be composed of letters, digits, and underscores (see e.g. https://www.unidata.ucar.edu/support/help/MailArchives/netcdf/msg10684.html)

        # - replace "." with "_"
        variable_name = variable_name.replace(".", "_")
        
        # - replace "-" with "_"
        variable_name = variable_name.replace("-", "_")
    
    # converting it to a netcdf file
    # - initiate an object to write a netcdf file
    output_netcdf = out_nc.OutputNetcdf(inputMapFileName = input_pcr_map_file, \
                                        netcdf_format = netcdf_format,\
                                        netcdf_zlib = netcdf_zlib_option,\
                                        netcdf_attribute_dict = netcdf_global_attributes,\
                                        netcdf_attribute_description = None,\
                                        netcdf_y_orientation_from_top_bottom = netcdf_y_orientation_from_top_bottom)
    # - create the netcdf file
    output_netcdf.createNetCDF(ncFileName = output_netcdf_file, \
                               varName    = variable_name, \
                               varUnits   = variable_unit, \
                               date       = None
                               )                                    
    # - write to the netcdf file
    output_netcdf.data2NetCDF(ncFileName   = output_netcdf_file, \
                              shortVarName = variable_name, 
                              varField     = pcr.pcr2numpy(input_pcr_map, vos.MV), 
                              timeStamp    = None, 
                              posCnt       = None
                              )
    
    print("\n Done! \n")                          
                                        

def main():
    
    # get system arguments
    system_argument = sys.argv
    
    # input and output files
    if "-inp" in system_argument:
        input_pcr_map_file = system_argument[system_argument.index("-inp") + 1]
    else:
        print("Please define an input of input_pcr_map_file with the argument -inp <input_pcr_map_file>.")
    if "-out" in system_argument:
        output_netcdf_file = system_argument[system_argument.index("-out") + 1]
    else:
        print("Please define an input of output_netcdf_file with the argument -out <output_netcdf_file>.")
    
    # optional arguments for variable name and unit
    variable_name = None
    variable_unit = "unknown"
    if "-var" in system_argument: variable_name = system_argument[system_argument.index("-var") + 1]
    if "-unt" in system_argument: variable_unit = system_argument[system_argument.index("-unt") + 1]
		
    # up to now, the following items are fixes    
    netcdf_global_attributes = None
    netcdf_y_orientation_from_top_bottom = True
    netcdf_format = "NETCDF4"
    netcdf_zlib_option = False
    time_input = None
    
    convert_pcraster_to_netcdf(\
                               input_pcr_map_file,\
                               output_netcdf_file,\
                               variable_name,\
                               netcdf_global_attributes,\
                               netcdf_y_orientation_from_top_bottom,\
                               variable_unit,\
                               netcdf_format,\
                               netcdf_zlib_option,\
                               time_input\
                               )

if __name__ == '__main__':
    sys.exit(main())
