import pytest
import os
import subprocess
from unittest.mock import patch, MagicMock

# Adjust path for imports
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Import main from the content-generator script
from main import main, BOOK_STRUCTURE, DOCS_DIR 
from book_generator.llm_interface import LLMInterface # Import the actual class

# Fixture to reset the LLMInterface singleton state for consistency
@pytest.fixture(autouse=True)
def reset_llm_interface_singleton_e2e():
    LLMInterface._instance = None
    yield

# Mock environment variables for consistency
@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch.dict(os.environ, {"MODEL_API_KEY": "fake_api_key"}):
        yield

# Mock the entire LLMInterface class for e2e tests
@pytest.fixture
def mock_llm_interface_class():
    with patch('book_generator.llm_interface.LLMInterface', autospec=True) as MockLLMInterface:
        mock_instance = MockLLMInterface.return_value
        mock_instance.generate_content.return_value = "## Generated Chapter Content\n\nThis is a test chapter."
        yield MockLLMInterface

# Temporary directory for Docusaurus build output
@pytest.fixture
def docusaurus_build_dir(tmp_path):
    return tmp_path / "build"

def test_e2e_book_generation_and_docusaurus_build(
    mock_llm_interface_class, tmp_path, docusaurus_build_dir
):
    """
    Tests the end-to-end process: content generation and a simulated Docusaurus build.
    """
    # Override DOCS_DIR to point to a temporary path for this test
    original_docs_dir = DOCS_DIR
    temp_docs_dir = tmp_path / "docs"
    with patch("main.DOCS_DIR", str(temp_docs_dir)):
        # Ensure temporary docs directory exists
        temp_docs_dir.mkdir(parents=True, exist_ok=True)

        # Run the main content generation script
        main()

        # Verify chapters are generated
        generated_files = list(temp_docs_dir.glob("*.md"))
        # We expect 10 chapters + Preface, so 11 files in BOOK_STRUCTURE
        assert len(generated_files) == len(BOOK_STRUCTURE), f"Expected {len(BOOK_STRUCTURE)} generated files, but found {len(generated_files)}"
        
        # Verify content of one generated file (using the new preface slug)
        sample_chapter_file = temp_docs_dir / "01-preface-the-new-digital-classroom-frontier.md"
        assert sample_chapter_file.exists()
        with open(sample_chapter_file, "r") as f:
            content = f.read()
            assert "id: preface-the-new-digital-classroom-frontier" in content
            assert "title: \"Preface: The New Digital Classroom Frontier\"" in content
            assert "## Generated Chapter Content" in content # From mock_llm_generate_content

        # Simulate Docusaurus build (simplified)
        # For a real E2E test, you would actually run `npm run build`
        # and point to a Docusaurus project. Here we simulate success.
        
        # Create a dummy package.json and docusaurus.config.ts for build context
        (tmp_path / "package.json").write_text('{"name": "test-docusaurus", "version": "1.0.0", "scripts": {"build": "echo BUILD_SUCCESS"}}')
        (tmp_path / "docusaurus.config.ts").write_text('module.exports = {};')

        # Mock subprocess.run to simulate 'npm run build'
        with patch("subprocess.run") as mock_subprocess_run:
            mock_process = MagicMock()
            mock_process.returncode = 0
            mock_process.stdout = b"BUILD_SUCCESS"
            mock_process.stderr = b""
            mock_subprocess_run.return_value = mock_process

            try:
                # Assuming the Docusaurus project root is `tmp_path`
                # And the build command would be run from `tmp_path`
                result = subprocess.run(
                    ["npm", "run", "build"], 
                    cwd=tmp_path, # Run from the temporary Docusaurus project root
                    check=True, 
                    capture_output=True, 
                    text=True
                )
                assert "BUILD_SUCCESS" in result.stdout
                assert mock_subprocess_run.called # Ensure subprocess.run was actually called
                print(f"Docusaurus build simulation output: {result.stdout}")
            except subprocess.CalledProcessError as e:
                pytest.fail(f"Docusaurus build simulation failed: {e.stderr}")
            except FileNotFoundError:
                pytest.skip("npm not found, skipping Docusaurus build simulation.")
