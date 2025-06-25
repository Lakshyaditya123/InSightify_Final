import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Navbar } from '../../components/navbar/navbar';
import { IdeaDetails } from '../../components/idea-details/idea-details'; // Adjust path as needed

@Component({
  selector: 'app-homescreen',
  standalone: true,
  imports: [CommonModule, Navbar, IdeaDetails],
  templateUrl: './homescreen.html',  // Updated to match separate file
  styleUrl: './homescreen.css'       // Updated to match separate file
})
export class Homescreen {
  selectedCard: any = null;

  ideaCards = [
    {
      id: 1,
      title: 'AI Assistant',
      subject: 'An intelligent assistant for daily tasks.',
      upvotes: 15,
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
      comments: 6,
      size: 'large',
      description: 'A secure digital vault for storing and organizing ideas with AI-powered categorization, similarity detection, and collaborative features.',
      author: 'Emily Davis',
      createdDate: '2024-03-12',
      tags: ['AI', 'Organization', 'Security']
    }
  ];

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
}
