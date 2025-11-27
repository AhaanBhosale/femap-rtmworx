# Python libraries
import itertools

# Import relevant SALT libraries
def create_library_import(file):
    content = """
    // Importing relevant SALT libraries
    const import, print = ::import, ::print;
    var rtwxlib = import'rtwxlib';
    var string = import'string';

    """
    file.write(content)
    return


# Create a monitor object in SALT
def create_monitor(file):
    content = """
    // Creating a monitor object
    const monitor = rtwxlib.Monitor
    {
        EvActivate = func() { print "Activate\\n"; };
        EvShutdown = func() { print "Shutdown\\n"; };
        EvProgress = func(self, fDone, msg = "") {
		    print("Progress: %d %s \\r"::format(fDone*100, msg));
    };
    EvEventMsg = func(self, msg) {
		print("\\nEvent: %s\\n"::format(msg));
        };
    };

"""
    file.write(content)
    return


# Create a solver object in SALT
def create_solver(file, filename):
    content = f"""
    // Creating a solver object
    var solver = rtwxlib.Solver(monitor);
    solver::Open("{filename}");
    solver::DelGeometry();

"""
    file.write(content)
    return

# Mesh the geometry
def mesh_geometry(file):
    content = """
    // Meshing the geometry
    const edgStats = solver::GetEdgeStats();
    const mshParams = solver::GetMeshParams();
    mshParams.edgMinSize = edgStats.crvLongest;
    mshParams.edgMaxSize = edgStats.crvLongest;
    solver::SetMeshParams(mshParams);
    solver::Remesh(true);
    """
    file.write(content)
    return

# Save and close file
def finalize_solver(file):
    content = """
    solver::SaveAs("Test.wrx");
    solver::Close();
    """
    file.write(content)
    return

# Create the SALT script
def create_salt_script(file_path, properties_list):

    # Write to file
    with open(file_path, 'w') as file:

        # Write library imports
        create_library_import(file)

        # Create monitor
        create_monitor(file)

        # Create solver
        create_solver(file, "runme.wrx")

        # Write each property to the SALT script
        for prop in properties_list:
            prop.write_salt_property(file)

        # Mesh the geometry
        mesh_geometry(file)

        # Finalize solver
        finalize_solver(file)


