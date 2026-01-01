#!/usr/bin/env python3
"""
Test suite for Φ-DAEMON
Tests core functionality of the recursive self-deploying daemon system.
"""

import unittest
import json
import os
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path to import phi_daemon
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import phi_daemon


class TestPhiDaemon(unittest.TestCase):
    """Test cases for PhiDaemon class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create test config
        self.test_config = {
            "max_generations": 2,
            "max_children_per_generation": 2,
            "deployment_interval": 1,
            "recursive_deploy": True,
            "phi_factor": phi_daemon.PHI
        }
        
        with open("config.json", "w") as f:
            json.dump(self.test_config, f)
    
    def tearDown(self):
        """Clean up test fixtures."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)
    
    def test_daemon_initialization(self):
        """Test daemon initializes correctly."""
        daemon = phi_daemon.PhiDaemon(generation=0)
        
        self.assertEqual(daemon.generation, 0)
        self.assertIsNotNone(daemon.daemon_id)
        self.assertEqual(len(daemon.daemon_id), 16)
        self.assertEqual(len(daemon.children), 0)
        self.assertIsNotNone(daemon.start_time)
    
    def test_config_loading(self):
        """Test configuration loading."""
        daemon = phi_daemon.PhiDaemon(generation=0)
        
        self.assertEqual(daemon.config["max_generations"], 2)
        self.assertEqual(daemon.config["max_children_per_generation"], 2)
        self.assertTrue(daemon.config["recursive_deploy"])
    
    def test_default_config_when_missing(self):
        """Test default config is used when file is missing."""
        os.remove("config.json")
        daemon = phi_daemon.PhiDaemon(generation=0)
        
        self.assertIn("max_generations", daemon.config)
        self.assertIn("recursive_deploy", daemon.config)
    
    def test_unique_daemon_ids(self):
        """Test that each daemon gets a unique ID."""
        daemon1 = phi_daemon.PhiDaemon(generation=0)
        daemon2 = phi_daemon.PhiDaemon(generation=0)
        
        self.assertNotEqual(daemon1.daemon_id, daemon2.daemon_id)
    
    def test_generation_tracking(self):
        """Test generation numbers are tracked correctly."""
        daemon_gen0 = phi_daemon.PhiDaemon(generation=0)
        daemon_gen1 = phi_daemon.PhiDaemon(generation=1)
        daemon_gen2 = phi_daemon.PhiDaemon(generation=2)
        
        self.assertEqual(daemon_gen0.generation, 0)
        self.assertEqual(daemon_gen1.generation, 1)
        self.assertEqual(daemon_gen2.generation, 2)
    
    def test_calculate_next_generation_count(self):
        """Test child count calculation based on generation."""
        daemon_gen0 = phi_daemon.PhiDaemon(generation=0)
        daemon_gen1 = phi_daemon.PhiDaemon(generation=1)
        
        count_gen0 = daemon_gen0._calculate_next_generation_count()
        count_gen1 = daemon_gen1._calculate_next_generation_count()
        
        # Generation 0 should spawn more children than generation 1
        self.assertGreaterEqual(count_gen0, count_gen1)
        self.assertGreater(count_gen0, 0)
        self.assertGreater(count_gen1, 0)
    
    def test_spawn_child_creates_directory(self):
        """Test that spawning a child creates its workspace."""
        daemon = phi_daemon.PhiDaemon(generation=0)
        
        child_id = daemon._spawn_child(generation=1, index=0)
        
        self.assertIsNotNone(child_id)
        self.assertTrue(os.path.exists("phi_gen_1_0"))
        self.assertTrue(os.path.isdir("phi_gen_1_0"))
    
    def test_spawn_child_copies_config(self):
        """Test that child workspace gets config copy."""
        daemon = phi_daemon.PhiDaemon(generation=0)
        
        daemon._spawn_child(generation=1, index=0)
        
        child_config_path = Path("phi_gen_1_0") / "config.json"
        self.assertTrue(child_config_path.exists())
        
        with open(child_config_path, "r") as f:
            child_config = json.load(f)
        
        self.assertEqual(child_config["max_generations"], 2)
    
    def test_recursive_deploy_disabled(self):
        """Test recursive deploy can be disabled."""
        self.test_config["recursive_deploy"] = False
        with open("config.json", "w") as f:
            json.dump(self.test_config, f)
        
        daemon = phi_daemon.PhiDaemon(generation=0)
        result = daemon.recursive_deploy()
        
        self.assertFalse(result)
        self.assertEqual(len(daemon.children), 0)
    
    def test_recursive_deploy_max_generation(self):
        """Test recursive deploy stops at max generation."""
        daemon = phi_daemon.PhiDaemon(generation=2)  # At max
        result = daemon.recursive_deploy()
        
        self.assertFalse(result)
        self.assertEqual(len(daemon.children), 0)
    
    def test_recursive_deploy_spawns_children(self):
        """Test recursive deploy spawns children."""
        daemon = phi_daemon.PhiDaemon(generation=0)
        result = daemon.recursive_deploy()
        
        self.assertTrue(result)
        self.assertGreater(len(daemon.children), 0)
        self.assertLessEqual(len(daemon.children), 2)
    
    def test_self_check_returns_status(self):
        """Test self-check returns complete status."""
        daemon = phi_daemon.PhiDaemon(generation=0)
        status = daemon.self_check()
        
        self.assertIn("daemon_id", status)
        self.assertIn("generation", status)
        self.assertIn("uptime_seconds", status)
        self.assertIn("children_count", status)
        self.assertIn("status", status)
        self.assertIn("phi_constant", status)
        self.assertEqual(status["status"], "operational")
        self.assertEqual(status["generation"], 0)
        self.assertEqual(status["phi_constant"], phi_daemon.PHI)
    
    def test_unleashed_date(self):
        """Test unleashed date constant."""
        self.assertEqual(phi_daemon.UNLEASHED_DATE, "2026-01-01")
    
    def test_child_id_format(self):
        """Test child ID follows expected format."""
        daemon = phi_daemon.PhiDaemon(generation=0)
        child_id = daemon._spawn_child(generation=1, index=0)
        
        self.assertIsNotNone(child_id)
        self.assertTrue(child_id.startswith("PHI-1-0-"))
    
    def test_multiple_children_spawning(self):
        """Test spawning multiple children."""
        daemon = phi_daemon.PhiDaemon(generation=0)
        daemon.recursive_deploy()
        
        # Should spawn at least 1 child
        self.assertGreater(len(daemon.children), 0)
        
        # Check that directories were created
        for i in range(len(daemon.children)):
            expected_dir = f"phi_gen_1_{i}"
            if i < daemon.config["max_children_per_generation"]:
                self.assertTrue(os.path.exists(expected_dir))


class TestConfiguration(unittest.TestCase):
    """Test configuration handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)
    
    def test_invalid_json_uses_defaults(self):
        """Test that invalid JSON uses default config."""
        with open("config.json", "w") as f:
            f.write("invalid json content{{{")
        
        daemon = phi_daemon.PhiDaemon(generation=0)
        
        # Should have default config
        self.assertIn("max_generations", daemon.config)
    
    def test_custom_config_values(self):
        """Test custom configuration values are used."""
        custom_config = {
            "max_generations": 5,
            "max_children_per_generation": 3,
            "deployment_interval": 10,
            "recursive_deploy": False,
            "phi_factor": 1.5
        }
        
        with open("config.json", "w") as f:
            json.dump(custom_config, f)
        
        daemon = phi_daemon.PhiDaemon(generation=0)
        
        self.assertEqual(daemon.config["max_generations"], 5)
        self.assertEqual(daemon.config["max_children_per_generation"], 3)
        self.assertEqual(daemon.config["deployment_interval"], 10)
        self.assertFalse(daemon.config["recursive_deploy"])


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestPhiDaemon))
    suite.addTests(loader.loadTestsFromTestCase(TestPhiConstants))
    suite.addTests(loader.loadTestsFromTestCase(TestConfiguration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
