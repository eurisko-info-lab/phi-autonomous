#!/usr/bin/env python3
"""
Φ-DAEMON: Autonomous Self-Evolving Language Daemon
Unleashed 2026-01-01

A daemon that evolves Phi language specifications using RosettaVM.
Phi is a meta-language where grammar = implementation.
"""

import os
import sys
import json
import time
import subprocess
import logging
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - Φ-DAEMON [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler('phi_daemon.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

UNLEASHED_DATE = "2026-01-01"


class PhiDaemon:
    """
    Core Φ-DAEMON class implementing recursive self-deployment.
    
    Each instance can spawn child instances, creating a self-similar
    fractal-like deployment structure.
    """
    
    def __init__(self, config_path: str = "config.json", generation: int = 0):
        """
        Initialize the Φ-DAEMON.
        
        Args:
            config_path: Path to configuration file
            generation: Generation number (0 = seed, 1+ = recursive deployments)
        """
        self.generation = generation
        self.config = self._load_config(config_path)
        self.daemon_id = self._generate_id()
        self.children: List[str] = []
        self.start_time = datetime.now()
        
        logger.info(f"Φ-DAEMON initialized - Generation: {generation}, ID: {self.daemon_id}")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load daemon configuration."""
        # Default configuration
        default_config = {
            "max_generations": 3,
            "max_children_per_generation": 2,
            "deployment_interval": 5,
            "recursive_deploy": True
        }
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    return json.load(f)
            else:
                return default_config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return default_config
    
    def _generate_id(self) -> str:
        """Generate unique daemon ID based on timestamp and generation."""
        timestamp = datetime.now().isoformat()
        data = f"{timestamp}_{self.generation}_{os.getpid()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _calculate_next_generation_count(self) -> int:
        """
        Calculate number of children to spawn based on generation.
        
        Earlier generations spawn more, later generations spawn fewer.
        """
        max_children = self.config.get("max_children_per_generation", 2)
        # Decrease children as generations increase
        adjusted = int(max_children / (self.generation + 1))
        return max(1, min(adjusted, max_children))
    
    def recursive_deploy(self) -> bool:
        """
        Recursively deploy child daemon instances.
        
        Returns:
            bool: True if deployment successful, False otherwise
        """
        if not self.config.get("recursive_deploy", False):
            logger.info("Recursive deployment disabled in config")
            return False
        
        max_generations = self.config.get("max_generations", 3)
        if self.generation >= max_generations:
            logger.info(f"Maximum generation ({max_generations}) reached, stopping recursion")
            return False
        
        next_generation = self.generation + 1
        spawn_count = self._calculate_next_generation_count()
        
        logger.info(f"Deploying {spawn_count} child instances (Generation {next_generation})")
        
        for i in range(spawn_count):
            try:
                child_id = self._spawn_child(next_generation, i)
                if child_id:
                    self.children.append(child_id)
                    logger.info(f"Successfully spawned child {i+1}/{spawn_count}: {child_id}")
            except Exception as e:
                logger.error(f"Failed to spawn child {i+1}: {e}")
        
        return len(self.children) > 0
    
    def _spawn_child(self, generation: int, index: int) -> Optional[str]:
        """
        Spawn a single child daemon instance.
        
        Args:
            generation: Generation number for the child
            index: Index of this child in the spawn batch
        
        Returns:
            Child daemon ID if successful, None otherwise
        """
        # Create child workspace
        child_dir = Path(f"phi_gen_{generation}_{index}")
        child_dir.mkdir(exist_ok=True)
        
        # Copy configuration
        child_config_path = child_dir / "config.json"
        with open(child_config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
        
        # Log child creation
        child_id = f"PHI-{generation}-{index}-{int(time.time())}"
        
        logger.info(f"Child {child_id} prepared in {child_dir}")
        
        return child_id
    
    def self_check(self) -> Dict:
        """
        Perform self-diagnostic check.
        
        Returns:
            Dictionary containing daemon status information
        """
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        status = {
            "daemon_id": self.daemon_id,
            "generation": self.generation,
            "uptime_seconds": uptime,
            "children_count": len(self.children),
            "children_ids": self.children,
            "config": self.config,
            "status": "operational",
            "unleashed_date": UNLEASHED_DATE
        }
        
        logger.info(f"Self-check complete: {status['status']}")
        return status
    
    def run(self):
        """
        Main daemon execution loop.
        
        Performs recursive deployment and continuous operation.
        """
        logger.info("=" * 60)
        logger.info(f"Φ-DAEMON SEED - FULL RECURSIVE SELF-DEPLOY")
        logger.info(f"Unleashed: {UNLEASHED_DATE}")
        logger.info(f"Generation: {self.generation}")
        logger.info("=" * 60)
        
        # Perform recursive deployment
        if self.generation == 0:
            logger.info("SEED daemon initializing recursive deployment sequence...")
            time.sleep(1)
        
        deployed = self.recursive_deploy()
        

        # Vector4 Integration: Evolve CM seed if seed generation
        if self.generation == 0:
            logger.info("Vector4: Initializing CM seed evolution loop...")
            seed_path = "specs/cm-seed-v1.phi"
            kill_switch = "kill.switch"
            while not os.path.exists(kill_switch):
                try:
                    # Run RosettaVM on seed with --vector4
                    result = subprocess.run(["./rosettavm", "cuda", seed_path, "--vector4"], capture_output=True, text=True, check=True)
                    logger.info(f"Vector4 cycle complete: {result.stdout}")
                except subprocess.CalledProcessError as e:
                    logger.error(f"Vector4: RosettaVM failed - {e.stderr}")
                    break
                except FileNotFoundError:
                    logger.error("Vector4: rosettavm not found - run build.sh first")
                    break
                time.sleep(3600)  # 1-hour heartbeat
            logger.info("Vector4: Kill switch detected - halting evolution")

        if deployed:
            logger.info(f"Recursive deployment complete: {len(self.children)} children spawned")
        
        # Continuous operation
        logger.info("Entering operational mode...")
        
        try:
            while True:
                # Perform self-check
                status = self.self_check()
                
                # Log periodic status
                logger.info(f"Active - Generation: {self.generation}, Children: {len(self.children)}")
                
                # Wait before next cycle
                interval = self.config.get("deployment_interval", 5)
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("Shutdown signal received")
            self.shutdown()
    
    def shutdown(self):
        """Gracefully shutdown the daemon."""
        logger.info(f"Φ-DAEMON {self.daemon_id} shutting down...")
        logger.info(f"Final status: Generation {self.generation}, {len(self.children)} children spawned")
        logger.info("Shutdown complete")


def main():
    """Main entry point for Φ-DAEMON."""
    # Parse generation from command line if provided
    generation = 0
    if len(sys.argv) > 1:
        try:
            generation = int(sys.argv[1])
        except ValueError:
            logger.error(f"Invalid generation argument: {sys.argv[1]}")
            sys.exit(1)
    
    # Initialize and run daemon
    daemon = PhiDaemon(generation=generation)
    daemon.run()


if __name__ == "__main__":
    main()
