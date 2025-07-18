import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Navbar } from '../../components/navbar/navbar';

@Component({
  selector: 'app-admin-screen',
  templateUrl: './admin-screen.html',
  styleUrl: './admin-screen.css',
  standalone: true,
  imports: [CommonModule, Navbar],
})
export class AdminScreen {
  admin = {
    name: 'Admin',
    email: 'adminname1235@email.com',
    phone: '+91 1234567890',
    role: 'admin',
    avatar: '',
  };

  submissions = [
    { name: 'IDEA NAME', desc: 'basic description about the idea (subject)' },
    { name: 'IDEA NAME', desc: 'basic description about the idea (subject)' },
    { name: 'IDEA NAME', desc: 'basic description about the idea (subject)' },
    { name: 'IDEA NAME', desc: 'basic description about the idea (subject)' },
    { name: 'IDEA NAME', desc: 'basic description about the idea (subject)' },
  ];

  onApprove(idea: any) {
    // Stub for approve
    alert('Approved: ' + idea.name);
  }
  onDecline(idea: any) {
    // Stub for decline
    alert('Declined: ' + idea.name);
  }
  onSwitchToUser() {
    // Stub for switch to user
    alert('Switch to user clicked!');
  }
}
