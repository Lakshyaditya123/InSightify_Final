/**
 * @fileoverview This file defines the core interfaces for API responses and data models.
 * Using these interfaces ensures type safety across the application.
 */

import { HttpErrorResponse } from "@angular/common/http";

/**
 * A generic structure for all API responses from the backend.
 * This ensures consistency in handling server responses.
 */
export interface ApiResponse {
  errCode: number; // 0 for success, non-zero for errors
  message: string; // A descriptive message from the server
  data?: any       // list payload
  datarec?: any;   // dict payload
}


export interface Idea_small {
  user_details: {
    id: number,
    name: string,
    profile_picture: string
  },
  idea_details: {
    id: 7,
    title: string,
    subject: string,
    created_at: string,
    comments_count: number
  },
  vote_details: Vote
}

export interface User_idea_details{
   user_details: {
    id: number,
    name: string,
    profile_picture: string
  },
  idea_details: {
    id: number,
    title: string,
    subject: string
  }
}


export interface Merged_idea_small {
  user_idea_details: User_idea_details[]
  merged_idea_details:{
    id: number,
    title: string,
    subject: string,
    comments_count: number
  }
  vote_details: Vote
}

export interface My_idea {
  idea_id: number,
  title: string,
  subject: string,
  status: number,
  comments_count: number,
  total_votes: number
}

export interface Tags{
  id: number,
  name: string,
  description: string
}

export interface Vote{
user_vote_details:{
  vote_id: number,
  vote_type: number
  },
idea_vote_details: {
  upvotes: 0,
  downvotes: 0,
  total: 0
  }
}
export interface Idea_large {
  user_details: {
    id: number,
    name: string,
    email:string,
    profile_picture: string
  },
  idea_details: {
    id: number,
    title: string,
    subject: string,
    content: string,
    refine_content: string;
    tags_list: Tags[]
    link: string,
    file_path: string,
    created_at: string,
    comments_count: number
  },
  vote_details: Vote
}


export interface Merged_idea_large {
  user_idea_details: User_idea_details[],
  merged_idea_details: {
    id: number,
    title: string,
    subject: string,
    content: string,
    tags_list: Tags[],
    created_at: string,
    comments_count: number
  },
  vote_details: Vote
}


export interface CurrUser{
  user_id: number,
  user_name: string,
  user_email: string,
  user_mobile: string,
  user_profile_picture: string,
  user_bio: string,
  user_role: string[]
}