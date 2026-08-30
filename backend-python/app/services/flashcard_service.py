"""
Spaced Repetition Flashcard Service
"""

import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone, timedelta
import random

from ..models.database import (
    Flashcard, FlashcardDeck, CardReview
)


class SpacedRepetitionService:
    """Service for spaced repetition flashcards using SM-2 algorithm."""

    def __init__(self):
        self.decks: Dict[str, FlashcardDeck] = {}
        self.cards: Dict[str, Flashcard] = {}
        self.reviews: Dict[str, CardReview] = {}
        self.ease_factor = 2.5

    def create_deck(self, name: str, description: Optional[str] = None) -> FlashcardDeck:
        """Create a new flashcard deck."""
        deck_id = str(uuid.uuid4())
        deck = FlashcardDeck(
            id=deck_id,
            name=name,
            description=description,
            card_count=0,
            due_count=0,
            new_count=0,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        self.decks[deck_id] = deck
        return deck

    def add_card(
        self,
        deck_id: str,
        front: str,
        back: str,
        tags: Optional[List[str]] = None
    ) -> Flashcard:
        """Add a card to a deck."""
        card_id = str(uuid.uuid4())
        card = Flashcard(
            id=card_id,
            deck_id=deck_id,
            front=front,
            back=back,
            tags=tags or [],
            difficulty=self.ease_factor,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        self.cards[card_id] = card

        # Update deck count
        if deck_id in self.decks:
            self.decks[deck_id].card_count += 1
            self.decks[deck_id].updated_at = datetime.now(timezone.utc)

        return card

    def add_cards_from_notes(self, deck_id: str, notes: List[str]) -> int:
        """Auto-generate flashcards from notes."""
        cards_added = 0
        for note in notes:
            # Simple sentence splitting for front/back pairs
            sentences = note.split('. ')
            if len(sentences) >= 2:
                front = sentences[0].strip()
                back = '. '.join(sentences[1:]).strip()
                self.add_card(deck_id, front, back)
                cards_added += 1
            elif sentences:
                # If only one sentence, make the whole thing front
                # and ask for recall on back
                self.add_card(deck_id, sentences[0].strip(), "Recall the full content")
                cards_added += 1
        return cards_added

    def get_due_cards(
        self, deck_id: str, limit: int = 20
    ) -> List[Flashcard]:
        """Get cards due for review."""
        now = datetime.now(timezone.utc)
        due_cards = []

        for card in self.cards.values():
            if card.deck_id != deck_id:
                continue

            # Calculate next review date
            next_review = self._calculate_next_review(card)

            if next_review <= now:
                due_cards.append(card)

        # Sort by next review date
        due_cards.sort(key=lambda c: self._calculate_next_review(c))
        return due_cards[:limit]

    def record_review(
        self,
        card_id: str,
        quality: int,
        response_time_ms: int = 1000
    ) -> CardReview:
        """Record a review result using SM-2 algorithm."""
        card = self.cards.get(card_id)
        if not card:
            raise ValueError(f"Card not found: {card_id}")

        now = datetime.now(timezone.utc)

        # SM-2 algorithm
        review = self.reviews.get(card_id)
        if review:
            # Update ease factor
            ease_factor = review.ease_factor
            if quality < 3:
                ease_factor = max(1.3, ease_factor - 0.2)
            elif quality == 3:
                ease_factor = ease_factor  # Keep same
            elif quality == 4:
                ease_factor = min(2.5, ease_factor + 0.1)
            else:  # quality == 5
                ease_factor = min(2.5, ease_factor + 0.15)
        else:
            ease_factor = self.ease_factor

        # Calculate interval
        if quality < 3:
            # Reset: review again soon
            interval = 1
        else:
            if review:
                prev_interval = review.interval
            else:
                prev_interval = 0

            if quality == 3:
                interval = 1
            elif quality == 4:
                interval = prev_interval * 1 if prev_interval > 0 else 3
            else:  # quality == 5
                interval = prev_interval * 1 if prev_interval > 0 else 6
                # Multiply by ease factor for longer intervals
                interval = int(interval * ease_factor)

        next_review = now + timedelta(days=max(1, interval))

        # Create review record
        review_record = CardReview(
            id=str(uuid.uuid4()),
            card_id=card_id,
            session_id=str(uuid.uuid4()),
            quality=quality,
            interval=interval,
            ease_factor=ease_factor,
            reviewed_at=now,
            response_time_ms=response_time_ms,
        )
        self.reviews[card_id] = review_record

        # Update card
        card.difficulty = ease_factor
        card.updated_at = now

        return review_record

    def _calculate_next_review(self, card: Flashcard) -> datetime:
        """Calculate the next review date for a card."""
        review = self.reviews.get(card.id)
        if not review:
            return card.created_at  # New cards are immediately due

        next_review = review.reviewed_at + timedelta(days=max(1, review.interval))
        return next_review

    def get_review_stats(self, deck_id: str) -> Dict[str, Any]:
        """Get statistics for a deck."""
        deck = self.decks.get(deck_id)
        if not deck:
            return {"error": "Deck not found"}

        now = datetime.now(timezone.utc)
        cards = [c for c in self.cards.values() if c.deck_id == deck_id]

        due_count = sum(1 for c in cards if self._calculate_next_review(c) <= now)
        new_count = sum(1 for c in cards if c.id not in self.reviews)

        return {
            "deck_id": deck_id,
            "total_cards": len(cards),
            "due_count": due_count,
            "new_count": new_count,
            "mastered_count": len([c for c in cards if c.id in self.reviews]),
        }

    def get_learning_path(self, deck_id: str) -> List[str]:
        """Get cards ordered by learning path (new -> due -> review)."""
        now = datetime.now(timezone.utc)
        cards = [c for c in self.cards.values() if c.deck_id == deck_id]

        # Sort by: new (no review) -> due -> review schedule
        def sort_key(card):
            review = self.reviews.get(card.id)
            next_review = self._calculate_next_review(card)
            if not review:
                return (0, 0)  # New cards first
            elif next_review <= now:
                return (1, 0)  # Due cards next
            else:
                return (2, next_review.timestamp())  # Scheduled last

        return sorted(cards, key=sort_key)