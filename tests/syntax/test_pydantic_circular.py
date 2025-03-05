from wexample_helpers.test.classes.pydantic_circular_kernel import Kernel
from wexample_helpers.debug.debug_dump import DebugDump

def test_pydantic_circular():
    # Create a kernel which will automatically create its service
    kernel = Kernel(name="test_kernel", debug=True)
    
    # Verify circular reference
    assert kernel.service.kernel == kernel
    assert kernel.service.name == "test_kernel_service"
    
    # Debug dump both objects
    kernel_dump = DebugDump(kernel)
    kernel_dump.execute()
    
    service_dump = DebugDump(kernel.service)
    service_dump.execute()
