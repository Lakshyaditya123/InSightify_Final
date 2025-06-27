import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class Idea {
  private apiUrl = 'http://192.168.1.35:5490';

  constructor(private http: HttpClient) { }

  // Create a new idea
  createIdea(ideaData: any) {
    // This would call your backend API when implemented
    console.log(`Creating idea: ${ideaData.title}`);
    return Promise.resolve({success: true, idea: ideaData});
  }

  // Mock voting functionality for now (since backend voting API isn't implemented yet)
  upvoteIdea(ideaId: number, userId: number) {
    // This would call your backend voting API when implemented
    console.log(`Upvoting idea ${ideaId} by user ${userId}`);
    return Promise.resolve({ success: true, voteType: 1 });
  }

  downvoteIdea(ideaId: number, userId: number) {
    // This would call your backend voting API when implemented
    console.log(`Downvoting idea ${ideaId} by user ${userId}`);
    return Promise.resolve({ success: true, voteType: -1 });
  }

  removeVote(ideaId: number, userId: number) {
    // This would call your backend voting API when implemented
    console.log(`Removing vote for idea ${ideaId} by user ${userId}`);
    return Promise.resolve({ success: true, voteType: 0 });
  }
      private add_idea_url: any = `${this.apiUrl}/add_idea`;
    add_idea(payload:any){
    return this.http.post<any>(this.add_idea_url,payload)
  }
}
