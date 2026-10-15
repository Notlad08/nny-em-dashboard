"""
SDRtrunk Stream Handler

This module handles the connection to SDRtrunk and streaming of audio chunks.
It uses WebSocket to receive audio data and buffers chunks for processing.
"""

import asyncio
import json
import time
from typing import Optional, Dict, List
from dataclasses import dataclass

@dataclass
class AudioChunk:
    """Represents an audio chunk from SDRtrunk"""
    stream_id: str
    chunk_start: str
    chunk_end: str
    audio_data: bytes
    timestamp: str
    sample_rate: int = 16000
    channels: int = 1

class SDRtrunkStreamHandler:
    """
    Handles SDRtrunk stream connection and chunk processing.
    
    Responsibilities:
    - Connect to SDRtrunk WebSocket stream
    - Buffer incoming audio data into chunks
    - Trigger processing when chunks are ready
    """
    
    def __init__(self, stream_url: str, chunk_duration_ms: int = 30000):
        self.stream_url = stream_url
        self.chunk_duration_ms = chunk_duration_ms
        self.ws: Optional[Any] = None
        self.is_running = False
        
        # Chunk buffering
        self.chunks_buffer: List[bytes] = []
        self.chunk_counter = 0
        self.last_chunk_time = None
        
        # Stream metadata
        self.stream_id = None
        self.sample_rate = 16000  # Default
        self.channels = 1
    
    async def connect(self):
        """Connect to SDRtrunk stream"""
        # todo: implement WebSocket connection
        # self.ws = await websocket.connect(self.stream_url)
        print(f"Connected to SDRtrunk stream: {self.stream_url}")
        return True
    
    async def disconnect(self):
        """Disconnect from SDRtrunk stream"""
        if self.ws:
            await self.ws.close()
            self.ws = None
            print("Disconnected from SDRtrunk stream")
    
    async def process_stream(self):
        """Main stream processing loop"""
        self.is_running = True
        
        try:
            while self.is_running:
                try:
                    # Read chunk from stream
                    chunk_data = await self._read_chunk()
                    
                    if chunk_data:
                        # Process chunk
                        await self._process_chunk(chunk_data)
                        
                        # Update timing
                        self.chunk_counter += 1
                        self.last_chunk_time = time.time()
                        
                except Exception as e:
                    print(f"Stream error: {e}")
                    await asyncio.sleep(1)
                    
        except asyncio.CancelledError:
            print("Stream processing cancelled")
        finally:
            await self.disconnect()
    
    async def _read_chunk(self) -> Optional[bytes]:
        """Read audio chunk from stream"""
        if not self.ws:
            return None
        
        # Read chunk_size bytes (adjust based on sample rate and duration)
        chunk_size = self.sample_rate * self.chunk_duration_ms // 1000
        data = b""
        
        while len(data) < chunk_size and self.is_running:
            try:
                chunk = await self.ws.receive()
                data += chunk
            except Exception as e:
                print(f"Read error: {e}")
                break
        
        if len(data) > 0:
            return data
        return None
    
    async def _process_chunk(self, chunk_data: bytes):
        """Process incoming audio chunk"""
        # todo: implement chunk processing
        # 1. Save chunk to storage
        # 2. Send to transcription worker
        # 3. Update ingestion metadata
        
        print(f"Processed chunk {self.chunk_counter}")
    
    def stop(self):
        """Stop stream processing"""
        self.is_running = False
