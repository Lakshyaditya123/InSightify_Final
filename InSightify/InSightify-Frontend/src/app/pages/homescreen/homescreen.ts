import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Navbar } from '../../components/navbar/navbar';
import { IdeaDetails } from '../../components/idea-details/idea-details'; // Adjust path as needed
import { Idea } from '../../services/idea';
import {CreateAdd} from '../../components/create-add/create-add';
import {Comments} from '../../components/comments/comments';

@Component({
  selector: 'app-homescreen',
  standalone: true,
  imports: [CommonModule, Navbar, IdeaDetails, CreateAdd, Comments],
  templateUrl: './homescreen.html',  // Updated to match separate file
  styleUrl: './homescreen.css'       // Updated to match separate file
})
export class Homescreen {
  selectedCard: any = null;
  currentUserId = 1; // Mock user ID - replace with actual user ID from auth

  ideaCards = [
    {
      id: 1,
      title: 'AI Assistant',
      subject: 'An intelligent assistant for daily tasks.',
      upvotes: 15,
      downvotes: 2,
      totalVotes: 13,
      userVote: 0, // 1 for upvote, -1 for downvote, 0 for no vote
      comments: 4,
      size: 'small',
      description: 'A comprehensive AI assistant that helps users manage their daily tasks, schedule appointments, and provide intelligent recommendations.',
      author: 'John Doe',
      createdDate: '2024-01-15',
      tags: ['AI', 'Productivity', 'Assistant']
    },
    {
      id: 2,
      title: 'MORPHOS',
      subject: 'Emotion-based ambient system that adapts lighting and sound.',
      upvotes: 23,
      downvotes: 1,
      totalVotes: 22,
      userVote: 0,
      comments: 7,
      size: 'large',
      description: 'An innovative ambient system that uses emotion recognition to automatically adjust lighting, sound, and environmental settings to match the user\'s mood.',
      author: 'Jane Smith',
      createdDate: '2024-02-10',
      tags: ['IoT', 'Emotion Recognition', 'Smart Home']
    },
    {
      id: 3,
      title: 'EcoRun Tracker',
      subject: 'Track and reward eco-friendly running.',
      upvotes: 9,
      downvotes: 3,
      totalVotes: 6,
      userVote: 0,
      comments: 2,
      size: 'medium',
      description: 'A running app that tracks your carbon footprint reduction while running and rewards eco-friendly routes and behaviors.',
      author: 'Mike Johnson',
      createdDate: '2024-03-05',
      tags: ['Fitness', 'Environment', 'Tracking']
    },
    {
      id: 4,
      title: 'CodeCollab',
      subject: 'Real-time collaborative coding platform.',
      upvotes: 17,
      downvotes: 0,
      totalVotes: 17,
      userVote: 0,
      comments: 5,
      size: 'medium',
      description: 'A platform that enables developers to collaborate on code in real-time with features like live editing, voice chat, and integrated version control.',
      author: 'Sarah Wilson',
      createdDate: '2024-02-28',
      tags: ['Development', 'Collaboration', 'Real-time']
    },
    {
      id: 5,
      title: 'InSight Analyzer',
      subject: 'Insight generation engine using NLP + ML.',
      upvotes: 12,
      downvotes: 1,
      totalVotes: 11,
      userVote: 0,
      comments: 3,
      size: 'small',
      description: 'An advanced analytics tool that uses Natural Language Processing and Machine Learning to generate actionable insights from unstructured data.',
      author: 'David Brown',
      createdDate: '2024-01-22',
      tags: ['NLP', 'Machine Learning', 'Analytics']
    },
    {
      id: 6,
      title: 'Idea Vault',
      subject: 'Secure and smart idea repository with AI categorization.',
      upvotes: 19,
      downvotes: 2,
      totalVotes: 17,
      userVote: 0,
      comments: 6,
      size: 'large',
      description: 'A secure digital vault for storing and organizing ideas with AI-powered categorization, similarity detection, and collaborative features.',
      author: 'Emily Davis',
      createdDate: '2024-03-12',
      tags: ['AI', 'Organization', 'Security']
    }
  ];

  constructor(private ideaService: Idea) {}

  // Voting methods
  async upvoteIdea(idea: any) {
    if (idea.userVote === 1) {
      // If already upvoted, remove the vote
      await this.removeVote(idea);
    } else {
      // Upvote the idea
      try {
        const result = await this.ideaService.upvoteIdea(idea.id, this.currentUserId);
        if (result.success) {
          if (idea.userVote === -1) {
            // If was downvoted, remove downvote and add upvote
            idea.downvotes--;
            idea.totalVotes += 2;
          } else {
            // If no vote, just add upvote
            idea.totalVotes += 1;
          }
          idea.upvotes++;
          idea.userVote = 1;
        }
      } catch (error) {
        console.error('Error upvoting idea:', error);
      }
    }
  }

  async downvoteIdea(idea: any) {
    if (idea.userVote === -1) {
      // If already downvoted, remove the vote
      await this.removeVote(idea);
    } else {
      // Downvote the idea
      try {
        const result = await this.ideaService.downvoteIdea(idea.id, this.currentUserId);
        if (result.success) {
          if (idea.userVote === 1) {
            // If was upvoted, remove upvote and add downvote
            idea.upvotes--;
            idea.totalVotes -= 2;
          } else {
            // If no vote, just add downvote
            idea.totalVotes -= 1;
          }
          idea.downvotes++;
          idea.userVote = -1;
        }
      } catch (error) {
        console.error('Error downvoting idea:', error);
      }
    }
  }

  async removeVote(idea: any) {
    try {
      const result = await this.ideaService.removeVote(idea.id, this.currentUserId);
      if (result.success) {
        if (idea.userVote === 1) {
          idea.upvotes--;
          idea.totalVotes -= 1;
        } else if (idea.userVote === -1) {
          idea.downvotes--;
          idea.totalVotes += 1;
        }
        idea.userVote = 0;
      }
    } catch (error) {
      console.error('Error removing vote:', error);
    }
  }

  getVoteDisplay(totalVotes: number): string {
    if (totalVotes >= 1000) {
      return (totalVotes / 1000).toFixed(1) + 'k';
    }
    return totalVotes.toString();
  }

  getVoteColorClass(totalVotes: number): string {
    if (totalVotes > 0) return 'text-success';
    if (totalVotes < 0) return 'text-danger';
    return 'text-muted';
  }

  open_ticket_details_modal(card: any) {
    console.log("Opening modal for card:", card.title);
    this.selectedCard = card;
    console.log(card);

    const modalElement = document.getElementById('ticket_details_modal');
    if (modalElement) {
      const modal = new (window as any).bootstrap.Modal(modalElement, {
        backdrop: 'static',
        keyboard: false
      });
      modal.show();
    }
  }

  close_ticket_details_modal() {
    const modalElement = document.getElementById('ticket_details_modal');
    if (modalElement) {
      const modal = (window as any).bootstrap.Modal.getInstance(modalElement);
      if (modal) {
        modal.hide();
      }
    }
    // Clear selected card when modal closes
    this.selectedCard = null;
  }

  // Handle modal close event (when user clicks backdrop or X button)
  onModalHidden() {
    this.selectedCard = null;
  }

  // Comments Modal
  open_comments_modal(card: any) {
    this.selectedCard = card;
    const modalElement = document.getElementById('comments_modal');
    if (modalElement) {
      const modal = new (window as any).bootstrap.Modal(modalElement, {
        backdrop: 'static',
        keyboard: false
      });
      modal.show();
    }
  }

  close_comments_modal() {
    const modalElement = document.getElementById('comments_modal');
    if (modalElement) {
      const modal = (window as any).bootstrap.Modal.getInstance(modalElement);
      if (modal) {
        modal.hide();
      }
    }
  }

  // Add Idea Modal
  open_add_idea_modal() {
    const modalElement = document.getElementById('addIdea_modal');
    if (modalElement) {
      const modal = new (window as any).bootstrap.Modal(modalElement, {
        backdrop: 'static',
        keyboard: false
      });
      modal.show();
    }
  }

  close_add_idea_modal() {
    const modalElement = document.getElementById('addIdea_modal');
    if (modalElement) {
      const modal = (window as any).bootstrap.Modal.getInstance(modalElement);
      if (modal) {
        modal.hide();
      }
    }
  }

}
