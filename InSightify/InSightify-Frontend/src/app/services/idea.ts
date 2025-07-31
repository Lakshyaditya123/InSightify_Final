import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ApiResponse, RefineContent,  Add_idea, AddComment } from './api-interfaces';

@Injectable({
  providedIn: 'root'
})
export class IdeaService {
  private apiUrl = 'http://localhost:5490';

  private create_idea_url = `${this.apiUrl}/user/add_idea`;
  private vote_url = `${this.apiUrl}/user/vote_update`;
  private get_all_main_wall_url = `${this.apiUrl}/user/main_wall`;
  private get_idea_url = `${this.apiUrl}/idea_display`;
  private refine_content_url= `${this.apiUrl}/user/refine_idea`;
  private add_tag_url= `${this.apiUrl}/add_tag`
  private get_all_comments_url = `${this.apiUrl}/user/comment_display`;
  private add_comment_url = `${this.apiUrl}/user/add_comment`;
  private get_user_profile = `${this.apiUrl}/user_profile`;
  private get_admin_wall =`${this.apiUrl}/admin/main_wall`;
  private update_idea_status=`${this.apiUrl}/admin/update_idea_status`

  constructor(private http: HttpClient) {}

get_all_main_walls(user_id: number): Observable<any> {
  const params = { user_id };
  return this.http.get(this.get_all_main_wall_url, { params });
}

get_all_comments(
  user_id: number,
  idea_id: number | null = null,
  merged_idea_id: number | null = null
): Observable<any> {
  const params: any = { user_id };
  if (idea_id !== null) params.idea_id = idea_id;
  if (merged_idea_id !== null) params.merged_idea_id = merged_idea_id;

  return this.http.get(this.get_all_comments_url, { params });
}
get_idea(idea_id: number | null, merged_idea_id: number | null, user_id: number): Observable<ApiResponse> {
  let params: any = { user_id };

  if (idea_id !== null) {
    params.idea_id = idea_id;
  } else if (merged_idea_id !== null) {
    params.merged_idea_id = merged_idea_id;
  }

  return this.http.get<ApiResponse>(this.get_idea_url, { params });
}

  createIdea(payload: Partial<Add_idea>): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(this.create_idea_url, payload);
  }

  addComment(payload: AddComment): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(this.add_comment_url, payload);
  }

  // Define a flexible vote payload that can support either idea_id or merged_idea_id
  private isValidVotePayload(payload: any): payload is { user_id: number; vote_type: number; idea_id?: number; merged_idea_id?: number; comment_id?: number } {
    return (
      typeof payload.user_id === 'number' &&
      typeof payload.vote_type === 'number' &&
      (typeof payload.idea_id === 'number' || typeof payload.merged_idea_id === 'number' || typeof payload.comment_id === 'number')
    );
  }

  updateVote(payload: { user_id: number; vote_type: number; idea_id?: number; merged_idea_id?: number; comment_id?: number }): Observable<ApiResponse> {
    if (!this.isValidVotePayload(payload)) {
      throw new Error("Invalid vote payload");
    }
    return this.http.post<ApiResponse>(this.vote_url, payload);
  }

  refineIdea(content:string): Observable<ApiResponse> {
    const params = { content };
  return this.http.get<ApiResponse>(this.refine_content_url, { params });
  }
  addNewTag(payload: { name: string, description: string }): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(this.add_tag_url, payload);
  }

  user_profile(user_id: number):Observable<ApiResponse> {
    const params= { user_id }
    return this.http.get<ApiResponse>(this.get_user_profile, { params })
  }
  get_all_admin_main_walls(): Observable<any> {
  return this.http.get(this.get_admin_wall);
} 
  update_user_idea(payload:any):Observable<any>{
    return this.http.post(this.update_idea_status,payload)
  }

}
