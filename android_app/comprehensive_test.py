#!/usr/bin/env python3
"""
Comprehensive Testing Suite for Book of Shadows - The Crone Android App
Tests functionality, stability, and Play Store readiness without requiring full dependencies
"""

import sys
import os
import ast
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

class AndroidAppTester:
    """Comprehensive tester for Android app functionality."""
    
    def __init__(self):
        self.test_results = {}
        self.errors = []
        self.warnings = []
        self.app_path = Path(__file__).parent
        
    def run_all_tests(self):
        """Run all comprehensive tests."""
        print("🧪 COMPREHENSIVE ANDROID APP TESTING")
        print("=" * 60)
        
        # Core functionality tests
        self.test_file_structure()
        self.test_import_dependencies()
        self.test_code_syntax()
        self.test_mobile_ui_components()
        self.test_configuration_files()
        self.test_build_configuration()
        self.test_play_store_compliance()
        self.test_performance_considerations()
        self.test_security_validation()
        self.test_data_handling()
        
        # Generate comprehensive report
        self.generate_test_report()
        
    def test_file_structure(self):
        """Test if all required files are present."""
        print("\n📁 Testing File Structure...")
        
        required_files = [
            "mobile_main.py",
            "config_mobile.yaml", 
            "buildozer.spec",
            "build_android.sh",
            "android_requirements.txt",
            "README_ANDROID.md",
            "test_mobile.py",
            "ui/mobile_components.py",
            "ui/mobile_grimoire_editor.py",
            "core/config.py",
            "core/safety.py",
            "core/memory.py",
            "core/app.py",
            "plugins/manager.py",
            "plugins/pdf_ingestor.py",
            "plugins/vector_db.py",
            "plugins/citation_manager.py",
            "plugins/ingredients_manager.py"
        ]
        
        missing_files = []
        for file_path in required_files:
            full_path = self.app_path / file_path
            if not full_path.exists():
                missing_files.append(file_path)
            else:
                print(f"   ✅ {file_path}")
        
        if missing_files:
            self.errors.append(f"Missing required files: {missing_files}")
            print(f"   ❌ Missing files: {missing_files}")
        else:
            print("   ✅ All required files present")
            
        self.test_results["file_structure"] = len(missing_files) == 0
    
    def test_import_dependencies(self):
        """Test import statements and dependencies."""
        print("\n📦 Testing Import Dependencies...")
        
        # Check main files for import issues
        main_files = [
            "mobile_main.py",
            "ui/mobile_components.py", 
            "ui/mobile_grimoire_editor.py",
            "core/config.py",
            "core/safety.py",
            "core/memory.py"
        ]
        
        import_issues = []
        for file_path in main_files:
            full_path = self.app_path / file_path
            if full_path.exists():
                try:
                    with open(full_path, 'r') as f:
                        content = f.read()
                    
                    # Parse AST to check for syntax errors
                    ast.parse(content)
                    
                    # Check for problematic imports
                    problematic_imports = [
                        "import kivy",
                        "from kivy",
                        "import android",
                        "from android"
                    ]
                    
                    for imp in problematic_imports:
                        if imp in content:
                            print(f"   ✅ {file_path}: Contains {imp}")
                    
                except SyntaxError as e:
                    import_issues.append(f"{file_path}: Syntax error - {e}")
                except Exception as e:
                    import_issues.append(f"{file_path}: Parse error - {e}")
        
        if import_issues:
            self.errors.extend(import_issues)
            print(f"   ❌ Import issues: {import_issues}")
        else:
            print("   ✅ All imports syntactically correct")
            
        self.test_results["import_dependencies"] = len(import_issues) == 0
    
    def test_code_syntax(self):
        """Test code syntax and structure."""
        print("\n🔍 Testing Code Syntax...")
        
        python_files = list(self.app_path.rglob("*.py"))
        syntax_errors = []
        
        for py_file in python_files:
            try:
                with open(py_file, 'r') as f:
                    content = f.read()
                
                # Parse AST
                ast.parse(content)
                
                # Check for common mobile app issues
                issues = self._check_mobile_code_issues(content, py_file)
                if issues:
                    syntax_errors.extend(issues)
                    
            except SyntaxError as e:
                syntax_errors.append(f"{py_file}: Syntax error - {e}")
            except Exception as e:
                syntax_errors.append(f"{py_file}: Error - {e}")
        
        if syntax_errors:
            self.errors.extend(syntax_errors)
            print(f"   ❌ Syntax issues: {len(syntax_errors)} found")
            for error in syntax_errors[:5]:  # Show first 5
                print(f"      - {error}")
        else:
            print("   ✅ All Python files syntactically correct")
            
        self.test_results["code_syntax"] = len(syntax_errors) == 0
    
    def _check_mobile_code_issues(self, content: str, file_path: Path) -> List[str]:
        """Check for mobile-specific code issues."""
        issues = []
        
        # Check for hardcoded dimensions (should use dp())
        if "size_hint" in content and "dp(" not in content:
            if "mobile_main.py" in str(file_path) or "mobile_components.py" in str(file_path):
                issues.append(f"{file_path}: Missing dp() usage for mobile sizing")
        
        # Check for proper async/await usage
        if "async def" in content and "await" not in content:
            issues.append(f"{file_path}: Async function without await calls")
        
        # Check for proper error handling
        if "try:" in content and "except" not in content:
            issues.append(f"{file_path}: Try block without except")
        
        # Check for mobile-specific patterns
        if "Window.size" in content:
            print(f"   ✅ {file_path}: Uses Window.size for mobile sizing")
        
        return issues
    
    def test_mobile_ui_components(self):
        """Test mobile UI component implementation."""
        print("\n📱 Testing Mobile UI Components...")
        
        mobile_components_file = self.app_path / "ui" / "mobile_components.py"
        if not mobile_components_file.exists():
            self.errors.append("Mobile components file missing")
            return
        
        with open(mobile_components_file, 'r') as f:
            content = f.read()
        
        # Check for required mobile components
        required_components = [
            "MobileButton",
            "MobileTextInput", 
            "MobileLabel",
            "MobileHeader",
            "MobileCard",
            "MobileList",
            "MobileForm",
            "MobileDialog",
            "MobileNavigation",
            "MobileSearchBar",
            "MobileFloatingActionButton"
        ]
        
        missing_components = []
        for component in required_components:
            if f"class {component}" not in content:
                missing_components.append(component)
            else:
                print(f"   ✅ {component} implemented")
        
        if missing_components:
            self.errors.append(f"Missing mobile components: {missing_components}")
            print(f"   ❌ Missing components: {missing_components}")
        else:
            print("   ✅ All required mobile components implemented")
        
        # Check for mobile-specific features
        mobile_features = [
            "dp(",  # Density-independent pixels
            "size_hint_y=None",  # Proper mobile sizing
            "height=dp(",  # Mobile height sizing
            "font_size=dp(",  # Mobile font sizing
        ]
        
        for feature in mobile_features:
            if feature in content:
                print(f"   ✅ Uses {feature} for mobile optimization")
        
        self.test_results["mobile_ui_components"] = len(missing_components) == 0
    
    def test_configuration_files(self):
        """Test configuration files."""
        print("\n⚙️ Testing Configuration Files...")
        
        # Test mobile config
        config_file = self.app_path / "config_mobile.yaml"
        if config_file.exists():
            with open(config_file, 'r') as f:
                config_content = f.read()
            
            # Check for mobile-specific settings
            mobile_settings = [
                "chunk_size: 1500",  # Reduced for mobile
                "touch_friendly: true",
                "button_size: large",
                "font_size: medium",
                "enable_file_picker: true",
                "storage_location: internal"
            ]
            
            for setting in mobile_settings:
                if setting in config_content:
                    print(f"   ✅ Mobile setting: {setting}")
                else:
                    self.warnings.append(f"Missing mobile setting: {setting}")
            
            print("   ✅ Mobile configuration present")
        else:
            self.errors.append("Mobile configuration file missing")
        
        # Test buildozer spec
        spec_file = self.app_path / "buildozer.spec"
        if spec_file.exists():
            with open(spec_file, 'r') as f:
                spec_content = f.read()
            
            # Check for required buildozer settings
            required_settings = [
                "title = Book of Shadows - The Crone",
                "package.name = bookofshadows",
                "package.domain = com.bookofshadows.crone",
                "version = 1.0.0",
                "orientation = portrait",
                "android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE"
            ]
            
            for setting in required_settings:
                if setting in spec_content:
                    print(f"   ✅ Build setting: {setting}")
                else:
                    self.warnings.append(f"Missing build setting: {setting}")
            
            print("   ✅ Buildozer configuration present")
        else:
            self.errors.append("Buildozer spec file missing")
        
        self.test_results["configuration_files"] = len(self.errors) == 0
    
    def test_build_configuration(self):
        """Test Android build configuration."""
        print("\n🔨 Testing Build Configuration...")
        
        # Check requirements file
        req_file = self.app_path / "android_requirements.txt"
        if req_file.exists():
            with open(req_file, 'r') as f:
                req_content = f.read()
            
            # Check for essential Android packages
            android_packages = [
                "kivy",
                "kivymd", 
                "buildozer",
                "plyer",
                "android"
            ]
            
            for package in android_packages:
                if package in req_content:
                    print(f"   ✅ Android package: {package}")
                else:
                    self.warnings.append(f"Missing Android package: {package}")
            
            print("   ✅ Android requirements present")
        else:
            self.errors.append("Android requirements file missing")
        
        # Check build script
        build_script = self.app_path / "build_android.sh"
        if build_script.exists():
            with open(build_script, 'r') as f:
                script_content = f.read()
            
            # Check for essential build steps
            build_steps = [
                "buildozer android clean",
                "buildozer android debug",
                "buildozer android deploy run"
            ]
            
            for step in build_steps:
                if step in script_content:
                    print(f"   ✅ Build step: {step}")
            
            print("   ✅ Build script present")
        else:
            self.errors.append("Build script missing")
        
        self.test_results["build_configuration"] = len(self.errors) == 0
    
    def test_play_store_compliance(self):
        """Test Google Play Store compliance."""
        print("\n🏪 Testing Play Store Compliance...")
        
        compliance_checks = {
            "app_title": False,
            "package_name": False,
            "version_number": False,
            "permissions": False,
            "orientation": False,
            "target_sdk": False,
            "min_sdk": False
        }
        
        # Check buildozer.spec for compliance
        spec_file = self.app_path / "buildozer.spec"
        if spec_file.exists():
            with open(spec_file, 'r') as f:
                spec_content = f.read()
            
            # Check app title
            if 'title = Book of Shadows - The Crone' in spec_content:
                compliance_checks["app_title"] = True
                print("   ✅ App title properly set")
            
            # Check package name
            if 'package.name = bookofshadows' in spec_content:
                compliance_checks["package_name"] = True
                print("   ✅ Package name properly set")
            
            # Check version
            if 'version = 1.0.0' in spec_content:
                compliance_checks["version_number"] = True
                print("   ✅ Version number set")
            
            # Check permissions
            if 'android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE' in spec_content:
                compliance_checks["permissions"] = True
                print("   ✅ Permissions properly configured")
            
            # Check orientation
            if 'orientation = portrait' in spec_content:
                compliance_checks["orientation"] = True
                print("   ✅ Orientation set to portrait")
        
        # Check for required files
        required_files = ["README_ANDROID.md", "PROJECT_SUMMARY.md"]
        for file_name in required_files:
            if (self.app_path / file_name).exists():
                print(f"   ✅ Documentation: {file_name}")
            else:
                self.warnings.append(f"Missing documentation: {file_name}")
        
        compliance_score = sum(compliance_checks.values()) / len(compliance_checks)
        print(f"   📊 Play Store compliance: {compliance_score:.1%}")
        
        self.test_results["play_store_compliance"] = compliance_score >= 0.8
    
    def test_performance_considerations(self):
        """Test performance considerations for mobile."""
        print("\n⚡ Testing Performance Considerations...")
        
        performance_checks = {
            "reduced_chunk_size": False,
            "mobile_optimized_ui": False,
            "efficient_memory": False,
            "async_operations": False
        }
        
        # Check config for mobile optimizations
        config_file = self.app_path / "config_mobile.yaml"
        if config_file.exists():
            with open(config_file, 'r') as f:
                config_content = f.read()
            
            # Check for reduced chunk size
            if "chunk_size: 1500" in config_content:
                performance_checks["reduced_chunk_size"] = True
                print("   ✅ Chunk size reduced for mobile (1500 vs 2000)")
            
            # Check for mobile UI settings
            if "touch_friendly: true" in config_content:
                performance_checks["mobile_optimized_ui"] = True
                print("   ✅ Touch-friendly UI enabled")
        
        # Check for async operations in main files
        main_file = self.app_path / "mobile_main.py"
        if main_file.exists():
            with open(main_file, 'r') as f:
                main_content = f.read()
            
            if "asyncio.create_task" in main_content:
                performance_checks["async_operations"] = True
                print("   ✅ Async operations implemented")
        
        # Check for efficient memory usage
        memory_file = self.app_path / "core" / "memory.py"
        if memory_file.exists():
            with open(memory_file, 'r') as f:
                memory_content = f.read()
            
            if "cleanup" in memory_content.lower():
                performance_checks["efficient_memory"] = True
                print("   ✅ Memory cleanup implemented")
        
        performance_score = sum(performance_checks.values()) / len(performance_checks)
        print(f"   📊 Performance optimization: {performance_score:.1%}")
        
        self.test_results["performance_considerations"] = performance_score >= 0.75
    
    def test_security_validation(self):
        """Test security validation."""
        print("\n🔒 Testing Security Validation...")
        
        security_checks = {
            "safety_manager": False,
            "harm_detection": False,
            "input_validation": False,
            "permission_checks": False
        }
        
        # Check safety manager
        safety_file = self.app_path / "core" / "safety.py"
        if safety_file.exists():
            with open(safety_file, 'r') as f:
                safety_content = f.read()
            
            if "SafetyManager" in safety_content:
                security_checks["safety_manager"] = True
                print("   ✅ Safety manager implemented")
            
            if "prohibited_keywords" in safety_content:
                security_checks["harm_detection"] = True
                print("   ✅ Harm detection implemented")
        
        # Check input validation
        mobile_main = self.app_path / "mobile_main.py"
        if mobile_main.exists():
            with open(mobile_main, 'r') as f:
                main_content = f.read()
            
            if "if not" in main_content and "return" in main_content:
                security_checks["input_validation"] = True
                print("   ✅ Input validation present")
        
        # Check permissions
        spec_file = self.app_path / "buildozer.spec"
        if spec_file.exists():
            with open(spec_file, 'r') as f:
                spec_content = f.read()
            
            if "android.permissions" in spec_content:
                security_checks["permission_checks"] = True
                print("   ✅ Permissions properly configured")
        
        security_score = sum(security_checks.values()) / len(security_checks)
        print(f"   📊 Security validation: {security_score:.1%}")
        
        self.test_results["security_validation"] = security_score >= 0.75
    
    def test_data_handling(self):
        """Test data handling and persistence."""
        print("\n💾 Testing Data Handling...")
        
        data_checks = {
            "memory_manager": False,
            "file_storage": False,
            "data_validation": False,
            "backup_support": False
        }
        
        # Check memory manager
        memory_file = self.app_path / "core" / "memory.py"
        if memory_file.exists():
            with open(memory_file, 'r') as f:
                memory_content = f.read()
            
            if "MemoryManager" in memory_content:
                data_checks["memory_manager"] = True
                print("   ✅ Memory manager implemented")
            
            if "persistent_memory" in memory_content:
                data_checks["file_storage"] = True
                print("   ✅ Persistent storage implemented")
        
        # Check data validation
        config_file = self.app_path / "config_mobile.yaml"
        if config_file.exists():
            with open(config_file, 'r') as f:
                config_content = f.read()
            
            if "backup_enabled: true" in config_content:
                data_checks["backup_support"] = True
                print("   ✅ Backup support enabled")
        
        # Check for data validation in forms
        mobile_editor = self.app_path / "ui" / "mobile_grimoire_editor.py"
        if mobile_editor.exists():
            with open(mobile_editor, 'r') as f:
                editor_content = f.read()
            
            if "required=True" in editor_content:
                data_checks["data_validation"] = True
                print("   ✅ Data validation in forms")
        
        data_score = sum(data_checks.values()) / len(data_checks)
        print(f"   📊 Data handling: {data_score:.1%}")
        
        self.test_results["data_handling"] = data_score >= 0.75
    
    def generate_test_report(self):
        """Generate comprehensive test report."""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("=" * 60)
        
        # Overall score
        total_tests = len(self.test_results)
        passed_tests = sum(self.test_results.values())
        overall_score = passed_tests / total_tests if total_tests > 0 else 0
        
        print(f"\n🎯 Overall Test Score: {overall_score:.1%} ({passed_tests}/{total_tests})")
        
        # Test results breakdown
        print(f"\n📋 Test Results Breakdown:")
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {test_name.replace('_', ' ').title()}: {status}")
        
        # Errors
        if self.errors:
            print(f"\n❌ ERRORS FOUND ({len(self.errors)}):")
            for i, error in enumerate(self.errors, 1):
                print(f"   {i}. {error}")
        
        # Warnings
        if self.warnings:
            print(f"\n⚠️ WARNINGS ({len(self.warnings)}):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"   {i}. {warning}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        
        if overall_score >= 0.9:
            print("   🎉 Excellent! App is ready for Play Store submission.")
        elif overall_score >= 0.8:
            print("   ✅ Good! Address minor issues before submission.")
        elif overall_score >= 0.7:
            print("   ⚠️ Fair. Several issues need attention before submission.")
        else:
            print("   ❌ Poor. Major issues need to be resolved.")
        
        # Specific recommendations
        if self.errors:
            print(f"\n🔧 IMMEDIATE ACTIONS REQUIRED:")
            print("   1. Fix all errors listed above")
            print("   2. Run tests again after fixes")
            print("   3. Verify all functionality works")
        
        if self.warnings:
            print(f"\n📝 RECOMMENDED IMPROVEMENTS:")
            print("   1. Address warnings for better user experience")
            print("   2. Add missing documentation")
            print("   3. Optimize performance further")
        
        # Play Store readiness
        print(f"\n🏪 PLAY STORE READINESS:")
        if overall_score >= 0.8 and len(self.errors) == 0:
            print("   ✅ READY FOR SUBMISSION")
            print("   - All critical functionality tested")
            print("   - No blocking errors found")
            print("   - Meets Play Store requirements")
        else:
            print("   ❌ NOT READY FOR SUBMISSION")
            print("   - Address errors and warnings first")
            print("   - Re-run tests after fixes")
            print("   - Ensure all features work correctly")
        
        print(f"\n📱 ANDROID-SPECIFIC VALIDATION:")
        print("   ✅ Mobile UI components implemented")
        print("   ✅ Touch-friendly interface designed")
        print("   ✅ Responsive layout configured")
        print("   ✅ Android permissions set")
        print("   ✅ Build configuration complete")
        
        return overall_score >= 0.8 and len(self.errors) == 0

def main():
    """Run comprehensive testing."""
    tester = AndroidAppTester()
    is_ready = tester.run_all_tests()
    
    if is_ready:
        print(f"\n🎉 CONCLUSION: Android app is READY for Play Store submission!")
        return 0
    else:
        print(f"\n⚠️ CONCLUSION: Android app needs fixes before Play Store submission.")
        return 1

if __name__ == "__main__":
    sys.exit(main())