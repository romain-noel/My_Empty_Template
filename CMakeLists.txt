cmake_minimum_required (VERSION 3.20)

#-----------------------------------------------------------------------
# Project info
#-----------------------------------------------------------------------

# Set parameters of the Project
set(PROJECT_NAME My_Empty_Template)
set(PROJECT_VERSION 1.2.0.1)
set(PROJECT_DESCRIPTION "A LaTeX template for simple but well organized documents.")
set(PROJECT_HOMEPAGE_URL "https://gitlab.com/irreductibles_gaulois/gothamSubThemes")
set(PROJECT_SITE_METHOD git) # wget, scp, git, svn, file, local 
set(PROJECT_DATE "2024.09.30")

# Project setup, versioning stuff here, change when changing the version
# Note: keep the project name lower case only for easy linux packaging support
project(${PROJECT_NAME} VERSION ${PROJECT_VERSION} LANGUAGES CXX) # LANGUAGES CXX
site_name(VERSION_HOST) # read hostname to VERSION_HOST
set(VERSION_HOST "${VERSION_HOST}" CACHE STRING "host of build" FORCE)

message(STATUS "")
message(STATUS "    == ${PROJECT_NAME} Project configuration == " )
message(STATUS "")

# Store the given value for the project.
set(${PROJECT_NAME}_NAME ${PROJECT_NAME})
set(${PROJECT_NAME}_VERSION ${PROJECT_VERSION})
set(${PROJECT_NAME}_DESCRIPTION ${PROJECT_DESCRIPTION})
set(${PROJECT_NAME}_HOMEPAGE_URL ${PROJECT_HOMEPAGE_URL})
set(${PROJECT_NAME}_SITE_METHOD ${PROJECT_SITE_METHOD})
set(${PROJECT_NAME}_DATE ${PROJECT_DATE})


#-----------------------------------------------------------------------
# General settings
#-----------------------------------------------------------------------

# Check if this project is the master project or a slave.
if(PROJECT_SOURCE_DIR STREQUAL CMAKE_SOURCE_DIR)
    set(${PROJECT_NAME}_MASTER_PROJECT ON)
endif()

# We can use include() and find_package() for our scripts in there
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/sources)
# include(projectSetting)

# Set the compiler
find_package(LATEX REQUIRED)
include(${CMAKE_MODULE_PATH}/UseLATEX.cmake) #https://gitlab.kitware.com/kmorel/UseLATEX


#-----------------------------------------------------------------------
#    My LaTeX variables
#-----------------------------------------------------------------------

# List of base directories to search in
set(BASE_DIRS
    "${CMAKE_SOURCE_DIR}/parts"
    "${CMAKE_SOURCE_DIR}/resources"
    "${CMAKE_SOURCE_DIR}/supplies"
    "${CMAKE_SOURCE_DIR}/sources"
)
set(MAIN_TEX_FILES
    "main.tex"
)
set(LIST_BIB_FILES "resources/ref_RN.bib" "resources/ref_XX.bib")
set(My_Biblatex "") # USE_BIBLATEX or empty=OFF => bibtex
set(My_pdf "FORCE_PDF") # add the `#` to set OFF
# set(LATEX_OUTPUT_PATH "${CMAKE_SOURCE_DIR}" ) # Build in tree (NOT RECOMMENDED)
# set(PDFLATEX_COMPILER "lualatex")
set(LATEX_POSTBUILD_OUTDIR_PATH "${CMAKE_SOURCE_DIR}/outdir" ) #
# Custom target to move generated PDFs to the LATEX_POSTBUILD_OUTDIR_PATH
message(STATUS " = =")

#-----------------------------------------------------------------------
#   Internal mechanisms
#-----------------------------------------------------------------------

# Function to make a path relative to CMAKE_SOURCE_DIR
function(make_relative output_var absolute_path)
    file(RELATIVE_PATH _rel_path "${CMAKE_SOURCE_DIR}" "${absolute_path}")
    set(${output_var} "${_rel_path}" PARENT_SCOPE)
endfunction()

# Initialize the two lists: one for files, one for directories
set(LIST_INPUTS_FILES "")
# set(LIST_INCLUDE_DIRS "${BASE_DIRS}")
foreach(SUBDIR ${BASE_DIRS})
    if(IS_DIRECTORY ${SUBDIR})  # Only add directories
        make_relative(REL_DIR ${SUBDIR})
        list(APPEND LIST_INCLUDE_DIRS ${REL_DIR})
    endif()
endforeach()

# Loop through base directories
foreach(DIR ${BASE_DIRS})
    # Add all .tex files in this directory and its subdirectories
    file(GLOB_RECURSE TEX_FILES "${DIR}/*.*")

    # Convert TEX_FILES to relative paths and append to LIST_INPUTS_FILES
    foreach(FILE ${TEX_FILES})
        make_relative(REL_FILE ${FILE})
        list(APPEND LIST_INPUTS_FILES ${REL_FILE})
    endforeach()

    # Add the current directory and its subdirectories
    file(GLOB_RECURSE DIRS LIST_DIRECTORIES true "${DIR}/*")

    # Convert DIRS to relative paths and append to LIST_INCLUDE_DIRS
    foreach(SUBDIR ${DIRS})
        if(IS_DIRECTORY ${SUBDIR})  # Only add directories
            make_relative(REL_DIR ${SUBDIR})
            list(APPEND LIST_INCLUDE_DIRS ${REL_DIR})
        endif()
    endforeach()
endforeach()

# Remove duplicate directories in LIST_INCLUDE_DIRS
list(REMOVE_DUPLICATES LIST_INCLUDE_DIRS)
list(REMOVE_ITEM LIST_INPUTS_FILES ${MAIN_TEX_FILES})

# Display the collected files and directories
message(STATUS "Input Files (Relative): ${LIST_INPUTS_FILES}")
message(STATUS "Include Directories (Relative): ${LIST_INCLUDE_DIRS}")


# 
foreach(FILE ${MAIN_TEX_FILES})
    add_latex_document(
        ${FILE}
        INPUTS  ${LIST_INPUTS_FILES}
        INCLUDE_DIRECTORIES  ${LIST_INCLUDE_DIRS}
        BIBFILES  ${LIST_BIB_FILES}
        ${My_pdf}  #FORCE_PDF
        ${My_Biblatex}  #USE_BIBLATEX
    )
endforeach()

foreach(FILE ${LIST_INPUTS_FILES})
    # Extract the file extension
    get_filename_component(FILE_EXT ${FILE} EXT)

    # Check if the file extension is .tex
    if(FILE_EXT STREQUAL ".tex")
        add_latex_document(
            ${FILE}
            INPUTS  ${LIST_INPUTS_FILES}
            INCLUDE_DIRECTORIES  ${LIST_INCLUDE_DIRS}
            BIBFILES  ${LIST_BIB_FILES}
            ${My_pdf}  #FORCE_PDF
            ${My_Biblatex}  #USE_BIBLATEX
            # DEPENDS generated_file.tex
            EXCLUDE_FROM_ALL
        )

        #  Here I should add a precommand to change the directory of compilation !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    endif()
endforeach()


# Function to list and print all CMake targets
function (get_all_cmake_targets out_var current_dir)
    # Get a list of all targets in the given directory.
    get_property(targets DIRECTORY ${current_dir} PROPERTY BUILDSYSTEM_TARGETS)
    get_property(subdirs DIRECTORY ${current_dir} PROPERTY SUBDIRECTORIES)

    # loop over folders 
    foreach(subdir ${subdirs})
        # recurrence
        get_all_cmake_targets(subdir_targets ${subdir})
        # add new found targets to the already found ones.
        list(APPEND targets ${subdir_targets})
    endforeach()

    # Copy the list found to the output variable.
    set(${out_var} "${targets}" PARENT_SCOPE)
endfunction()

# Run at end of top-level CMakeLists
get_all_cmake_targets( all_targets ${CMAKE_CURRENT_SOURCE_DIR} )
# message(STATUS "get_all_cmake_targets (all_targets): ${all_targets}")


# Custom target to move generated PDFs to the LATEX_POSTBUILD_OUTDIR_PATH
make_relative(REL_PB_OUTDIR ${LATEX_POSTBUILD_OUTDIR_PATH})
foreach(TGT ${all_targets})
    # Check if the file extension is .tex
    if(TGT MATCHES ".*_pdf")
        # Find the position of the underscore
        string(FIND ${TGT} "_pdf" UNDERSCORE_POS)
        # Extract the substring from the start to the position of the underscore
        string(SUBSTRING ${TGT} 0 ${UNDERSCORE_POS} TARGET_part)

        # Set for all target 'shell-escape'
        set_target_properties(
            ${TGT}
            PROPERTIES COMPILER_FLAGS "--shell-escape"
        )
        message(STATUS "Add '--shell-escape' flag to target: ${TGT}")

        # add_custom_target(CopyPDF ALL
        add_custom_command(
            TARGET ${TGT}
            POST_BUILD
            # COMMAND ${CMAKE_COMMAND} -E make_directory ${LATEX_POSTBUILD_OUTDIR_PATH}
            COMMAND ${CMAKE_COMMAND} -E copy_if_different "${CMAKE_BINARY_DIR}/${TARGET_part}.pdf" "${LATEX_POSTBUILD_OUTDIR_PATH}/${TARGET_part}.pdf"
            DEPENDS ${TGT}
            COMMENT "Copying generated ${TARGET_part}.pdf to /${REL_PB_OUTDIR}/${TARGET_part}.pdf"
        )
    endif()
endforeach()

# add_custom_command(
#     OUTPUT ${output_dir}/generated_file.tex
#     COMMAND tex_file_generate_exe
#     ARGS ${output_dir}/generated_file.tex
# )

# EoF