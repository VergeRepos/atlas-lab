"""Tests for flashcard service."""
import pytest
from app.services.flashcard_service import SpacedRepetitionService

def test_create_deck():
    svc = SpacedRepetitionService()
    deck = svc.create_deck("Test Deck", "A test deck")
    assert deck.name == "Test Deck"
    assert deck.id in svc.decks

def test_add_card():
    svc = SpacedRepetitionService()
    deck = svc.create_deck("Deck")
    card = svc.add_card(deck.id, "Front", "Back")
    assert card.front == "Front"
    assert card.back == "Back"
    assert card.id in svc.cards

def test_record_review_quality_4():
    svc = SpacedRepetitionService()
    deck = svc.create_deck("Deck")
    card = svc.add_card(deck.id, "Front", "Back")
    review = svc.record_review(card.id, quality=4)
    assert review.card_id == card.id
    assert review.quality == 4
    assert review.interval > 0

def test_record_review_quality_fail():
    svc = SpacedRepetitionService()
    deck = svc.create_deck("Deck")
    card = svc.add_card(deck.id, "Front", "Back")
    review = svc.record_review(card.id, quality=1)
    assert review.interval == 1

def test_get_due_cards():
    svc = SpacedRepetitionService()
    deck = svc.create_deck("Deck")
    card = svc.add_card(deck.id, "Front", "Back")
    due = svc.get_due_cards(deck.id)
    assert len(due) == 1
    assert due[0].id == card.id

def test_get_review_stats():
    svc = SpacedRepetitionService()
    deck = svc.create_deck("Deck")
    card = svc.add_card(deck.id, "Front", "Back")
    stats = svc.get_review_stats(deck.id)
    assert stats["total_cards"] == 1
    assert stats["new_count"] == 1
