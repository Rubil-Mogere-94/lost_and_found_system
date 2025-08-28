# app/cli.py
import click
from app.database import Session
from app.models import User, Item
from app.utils import get_user_by_id, get_item_by_id, user_exists
from datetime import datetime

@click.group()
def cli():
    """Digital Key Tracker CLI - Manage lost and found items"""
    pass

@cli.command()
@click.option('--name', prompt='Name', help='User full name')
@click.option('--email', prompt='Email', help='User email address')
@click.option('--role', prompt='Role (finder/claimer/admin)', 
              type=click.Choice(['finder', 'claimer', 'admin']), 
              help='User role')
def register(name, email, role):
    """Register a new user"""
    if user_exists(email):
        click.echo("Error: A user with this email already exists.")
        return
    
    session = Session()
    try:
        user = User(name=name, email=email, role=role)
        session.add(user)
        session.commit()
        click.echo(f"User registered successfully with ID: {user.id}")
    except Exception as e:
        session.rollback()
        click.echo(f"Error: {str(e)}")
    finally:
        Session.remove()

@cli.command()
@click.option('--user-id', prompt='User ID', type=int, help='ID of the user who found the item')
@click.option('--description', prompt='Description', help='Description of the found item')
@click.option('--location', prompt='Location', help='Location where the item was found')
def log_item(user_id, description, location):
    """Log a new found item"""
    user = get_user_by_id(user_id)
    if not user:
        click.echo("Error: User not found.")
        return
    
    session = Session()
    try:
        item = Item(
            description=description,
            location=location,
            finder_id=user_id
        )
        session.add(item)
        session.commit()
        click.echo(f"Item logged successfully with ID: {item.id}")
    except Exception as e:
        session.rollback()
        click.echo(f"Error: {str(e)}")
    finally:
        Session.remove()

@cli.command()
@click.option('--item-id', prompt='Item ID', type=int, help='ID of the item to claim')
@click.option('--user-id', prompt='User ID', type=int, help='ID of the user claiming the item')
def claim(item_id, user_id):
    """Claim a found item"""
    item = get_item_by_id(item_id)
    if not item:
        click.echo("Error: Item not found.")
        return
    
    user = get_user_by_id(user_id)
    if not user:
        click.echo("Error: User not found.")
        return
    
    if item.status == 'claimed':
        click.echo("Error: This item has already been claimed.")
        return
    
    session = Session()
    try:
        item.status = 'claimed'
        item.claimer_id = user_id
        item.date_claimed = datetime.utcnow()
        session.commit()
        click.echo(f"Item {item_id} successfully claimed by user {user_id}")
    except Exception as e:
        session.rollback()
        click.echo(f"Error: {str(e)}")
    finally:
        Session.remove()

@cli.command()
@click.option('--user-id', prompt='User ID', type=int, help='ID of the user')
def history(user_id):
    """View claim history for a user"""
    user = get_user_by_id(user_id)
    if not user:
        click.echo("Error: User not found.")
        return
    
    session = Session()
    try:
        claimed_items = session.query(Item).filter(Item.claimer_id == user_id).all()
        
        if not claimed_items:
            click.echo("No claimed items found for this user.")
            return
        
        click.echo(f"Claim history for {user.name}:")
        for item in claimed_items:
            click.echo(f"  - Item {item.id}: {item.description} (claimed on {item.date_claimed})")
    finally:
        Session.remove()

@cli.command()
@click.option('--item-id', prompt='Item ID', type=int, help='ID of the item to delete')
@click.option('--user-id', prompt='User ID', type=int, help='ID of the admin user')
def delete(item_id, user_id):
    """Delete an item (admin only)"""
    user = get_user_by_id(user_id)
    if not user or user.role != 'admin':
        click.echo("Error: Only admin users can delete items.")
        return
    
    item = get_item_by_id(item_id)
    if not item:
        click.echo("Error: Item not found.")
        return
    
    session = Session()
    try:
        session.delete(item)
        session.commit()
        click.echo(f"Item {item_id} deleted successfully.")
    except Exception as e:
        session.rollback()
        click.echo(f"Error: {str(e)}")
    finally:
        Session.remove()

@cli.command()
def list_users():
    """List all registered users"""
    session = Session()
    try:
        users = session.query(User).all()
        
        if not users:
            click.echo("No users found.")
            return
        
        click.echo("Registered users:")
        for user in users:
            click.echo(f"  {user.id}: {user.name} ({user.email}) - {user.role}")
    finally:
        Session.remove()

@cli.command()
def list_items():
    """List all items"""
    session = Session()
    try:
        items = session.query(Item).all()
        
        if not items:
            click.echo("No items found.")
            return
        
        click.echo("All items:")
        for item in items:
            status = f"claimed by user {item.claimer_id}" if item.status == 'claimed' else "unclaimed"
            click.echo(f"  {item.id}: {item.description} - {status}")
    finally:
        Session.remove()

if __name__ == '__main__':
    cli()