import requests
import random
import json
import math
import hashlib
import hmac
import urllib
import uuid
import time
import sys
#from __future__ import unicode_literals, absolute_import
#from datetime import datetime
import datetime
import logging
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
if sys.version_info.major == 3:
   import urllib.parse
import calendar
from task.models import instagram_follower


# The urllib library was split into other modules from Python 2 to Python 3
#if sys.version_info.major == 3:
    #import urllib.parse

class InstagramAPI:
    API_URL = 'https://i.instagram.com/api/v1/'
    #API_URL='https://www.instagram.com/accounts/login/'
    DEVICE_SETTINTS = {
        'manufacturer': 'Xiaomi',
        'model': 'HM 1SW',
        'android_version': 18,
        'android_release': '4.3'
    }
    USER_AGENT = 'Instagram 10.26.0 Android ({android_version}/{android_release}; 320dpi; 720x1280; {manufacturer}; {model}; armani; qcom; en_US)'.format(
        **DEVICE_SETTINTS)
    IG_SIG_KEY = '4f8732eb9ba7d1c8e8897a75d6474d4eb3f5279137431b2aafb71fafe2abe178'
    EXPERIMENTS = '''ig_promote_reach_objective_fix_universe,ig_android_universe_video_production,ig_search_client_h1_2017_holdout,ig_android_live_follow_from_comments_universe,ig_android_carousel_non_square_creation,ig_android_live_analytics,ig_android_follow_all_dialog_confirmation_copy,ig_android_stories_server_coverframe,ig_android_video_captions_universe,ig_android_offline_location_feed,ig_android_direct_inbox_retry_seen_state,ig_android_ontact_invite_universe,ig_android_live_broadcast_blacklist,ig_android_insta_video_reconnect_viewers,ig_android_ad_async_ads_universe,ig_android_search_clear_layout_universe,ig_android_shopping_reporting,ig_android_stories_surface_universe,ig_android_verified_comments_universe,ig_android_preload_media_ahead_in_current_reel,android_instagram_prefetch_suggestions_universe,ig_android_reel_viewer_fetch_missing_reels_universe,ig_android_direct_search_share_sheet_universe,ig_android_business_promote_tooltip,ig_android_direct_blue_tab,ig_android_async_network_tweak_universe,ig_android_elevate_main_thread_priority_universe,ig_android_stories_gallery_nux,ig_android_instavideo_remove_nux_comments,ig_video_copyright_whitelist,ig_react_native_inline_insights_with_relay,ig_android_direct_thread_message_animation,ig_android_draw_rainbow_client_universe,ig_android_direct_link_style,ig_android_live_heart_enhancements_universe,ig_android_rtc_reshare,ig_android_preload_item_count_in_reel_viewer_buffer,ig_android_users_bootstrap_service,ig_android_auto_retry_post_mode,ig_android_shopping,ig_android_main_feed_seen_state_dont_send_info_on_tail_load,ig_fbns_preload_default,ig_android_gesture_dismiss_reel_viewer,ig_android_tool_tip,ig_android_ad_logger_funnel_logging_universe,ig_android_gallery_grid_column_count_universe,ig_android_business_new_ads_payment_universe,ig_android_direct_links,ig_android_audience_control,ig_android_live_encore_consumption_settings_universe,ig_perf_android_holdout,ig_android_cache_contact_import_list,ig_android_links_receivers,ig_android_ad_impression_backtest,ig_android_list_redesign,ig_android_stories_separate_overlay_creation,ig_android_stop_video_recording_fix_universe,ig_android_render_video_segmentation,ig_android_live_encore_reel_chaining_universe,ig_android_sync_on_background_enhanced_10_25,ig_android_immersive_viewer,ig_android_mqtt_skywalker,ig_fbns_push,ig_android_ad_watchmore_overlay_universe,ig_android_react_native_universe,ig_android_profile_tabs_redesign_universe,ig_android_live_consumption_abr,ig_android_story_viewer_social_context,ig_android_hide_post_in_feed,ig_android_video_loopcount_int,ig_android_enable_main_feed_reel_tray_preloading,ig_android_camera_upsell_dialog,ig_android_ad_watchbrowse_universe,ig_android_internal_research_settings,ig_android_search_people_tag_universe,ig_android_react_native_ota,ig_android_enable_concurrent_request,ig_android_react_native_stories_grid_view,ig_android_business_stories_inline_insights,ig_android_log_mediacodec_info,ig_android_direct_expiring_media_loading_errors,ig_video_use_sve_universe,ig_android_cold_start_feed_request,ig_android_enable_zero_rating,ig_android_reverse_audio,ig_android_branded_content_three_line_ui_universe,ig_android_live_encore_production_universe,ig_stories_music_sticker,ig_android_stories_teach_gallery_location,ig_android_http_stack_experiment_2017,ig_android_stories_device_tilt,ig_android_pending_request_search_bar,ig_android_fb_topsearch_sgp_fork_request,ig_android_seen_state_with_view_info,ig_android_animation_perf_reporter_timeout,ig_android_new_block_flow,ig_android_story_tray_title_play_all_v2,ig_android_direct_address_links,ig_android_stories_archive_universe,ig_android_save_collections_cover_photo,ig_android_live_webrtc_livewith_production,ig_android_sign_video_url,ig_android_stories_video_prefetch_kb,ig_android_stories_create_flow_favorites_tooltip,ig_android_live_stop_broadcast_on_404,ig_android_live_viewer_invite_universe,ig_android_promotion_feedback_channel,ig_android_render_iframe_interval,ig_android_accessibility_logging_universe,ig_android_camera_shortcut_universe,ig_android_use_one_cookie_store_per_user_override,ig_profile_holdout_2017_universe,ig_android_stories_server_brushes,ig_android_ad_media_url_logging_universe,ig_android_shopping_tag_nux_text_universe,ig_android_comments_single_reply_universe,ig_android_stories_video_loading_spinner_improvements,ig_android_collections_cache,ig_android_comment_api_spam_universe,ig_android_facebook_twitter_profile_photos,ig_android_shopping_tag_creation_universe,ig_story_camera_reverse_video_experiment,ig_android_direct_bump_selected_recipients,ig_android_ad_cta_haptic_feedback_universe,ig_android_vertical_share_sheet_experiment,ig_android_family_bridge_share,ig_android_search,ig_android_insta_video_consumption_titles,ig_android_stories_gallery_preview_button,ig_android_fb_auth_education,ig_android_camera_universe,ig_android_me_only_universe,ig_android_instavideo_audio_only_mode,ig_android_user_profile_chaining_icon,ig_android_live_video_reactions_consumption_universe,ig_android_stories_hashtag_text,ig_android_post_live_badge_universe,ig_android_swipe_fragment_container,ig_android_search_users_universe,ig_android_live_save_to_camera_roll_universe,ig_creation_growth_holdout,ig_android_sticker_region_tracking,ig_android_unified_inbox,ig_android_live_new_watch_time,ig_android_offline_main_feed_10_11,ig_import_biz_contact_to_page,ig_android_live_encore_consumption_universe,ig_android_experimental_filters,ig_android_search_client_matching_2,ig_android_react_native_inline_insights_v2,ig_android_business_conversion_value_prop_v2,ig_android_redirect_to_low_latency_universe,ig_android_ad_show_new_awr_universe,ig_family_bridges_holdout_universe,ig_android_background_explore_fetch,ig_android_following_follower_social_context,ig_android_video_keep_screen_on,ig_android_ad_leadgen_relay_modern,ig_android_profile_photo_as_media,ig_android_insta_video_consumption_infra,ig_android_ad_watchlead_universe,ig_android_direct_prefetch_direct_story_json,ig_android_shopping_react_native,ig_android_top_live_profile_pics_universe,ig_android_direct_phone_number_links,ig_android_stories_weblink_creation,ig_android_direct_search_new_thread_universe,ig_android_histogram_reporter,ig_android_direct_on_profile_universe,ig_android_network_cancellation,ig_android_background_reel_fetch,ig_android_react_native_insights,ig_android_insta_video_audio_encoder,ig_android_family_bridge_bookmarks,ig_android_data_usage_network_layer,ig_android_universal_instagram_deep_links,ig_android_dash_for_vod_universe,ig_android_modular_tab_discover_people_redesign,ig_android_mas_sticker_upsell_dialog_universe,ig_android_ad_add_per_event_counter_to_logging_event,ig_android_sticky_header_top_chrome_optimization,ig_android_rtl,ig_android_biz_conversion_page_pre_select,ig_android_promote_from_profile_button,ig_android_live_broadcaster_invite_universe,ig_android_share_spinner,ig_android_text_action,ig_android_own_reel_title_universe,ig_promotions_unit_in_insights_landing_page,ig_android_business_settings_header_univ,ig_android_save_longpress_tooltip,ig_android_constrain_image_size_universe,ig_android_business_new_graphql_endpoint_universe,ig_ranking_following,ig_android_stories_profile_camera_entry_point,ig_android_universe_reel_video_production,ig_android_power_metrics,ig_android_sfplt,ig_android_offline_hashtag_feed,ig_android_live_skin_smooth,ig_android_direct_inbox_search,ig_android_stories_posting_offline_ui,ig_android_sidecar_video_upload_universe,ig_android_promotion_manager_entry_point_universe,ig_android_direct_reply_audience_upgrade,ig_android_swipe_navigation_x_angle_universe,ig_android_offline_mode_holdout,ig_android_live_send_user_location,ig_android_direct_fetch_before_push_notif,ig_android_non_square_first,ig_android_insta_video_drawing,ig_android_swipeablefilters_universe,ig_android_live_notification_control_universe,ig_android_analytics_logger_running_background_universe,ig_android_save_all,ig_android_reel_viewer_data_buffer_size,ig_direct_quality_holdout_universe,ig_android_family_bridge_discover,ig_android_react_native_restart_after_error_universe,ig_android_startup_manager,ig_story_tray_peek_content_universe,ig_android_profile,ig_android_high_res_upload_2,ig_android_http_service_same_thread,ig_android_scroll_to_dismiss_keyboard,ig_android_remove_followers_universe,ig_android_skip_video_render,ig_android_story_timestamps,ig_android_live_viewer_comment_prompt_universe,ig_profile_holdout_universe,ig_android_react_native_insights_grid_view,ig_stories_selfie_sticker,ig_android_stories_reply_composer_redesign,ig_android_streamline_page_creation,ig_explore_netego,ig_android_ig4b_connect_fb_button_universe,ig_android_feed_util_rect_optimization,ig_android_rendering_controls,ig_android_os_version_blocking,ig_android_encoder_width_safe_multiple_16,ig_search_new_bootstrap_holdout_universe,ig_android_snippets_profile_nux,ig_android_e2e_optimization_universe,ig_android_comments_logging_universe,ig_shopping_insights,ig_android_save_collections,ig_android_live_see_fewer_videos_like_this_universe,ig_android_show_new_contact_import_dialog,ig_android_live_view_profile_from_comments_universe,ig_fbns_blocked,ig_formats_and_feedbacks_holdout_universe,ig_android_reduce_view_pager_buffer,ig_android_instavideo_periodic_notif,ig_search_user_auto_complete_cache_sync_ttl,ig_android_marauder_update_frequency,ig_android_suggest_password_reset_on_oneclick_login,ig_android_promotion_entry_from_ads_manager_universe,ig_android_live_special_codec_size_list,ig_android_enable_share_to_messenger,ig_android_background_main_feed_fetch,ig_android_live_video_reactions_creation_universe,ig_android_channels_home,ig_android_sidecar_gallery_universe,ig_android_upload_reliability_universe,ig_migrate_mediav2_universe,ig_android_insta_video_broadcaster_infra_perf,ig_android_business_conversion_social_context,android_ig_fbns_kill_switch,ig_android_live_webrtc_livewith_consumption,ig_android_destroy_swipe_fragment,ig_android_react_native_universe_kill_switch,ig_android_stories_book_universe,ig_android_all_videoplayback_persisting_sound,ig_android_draw_eraser_universe,ig_direct_search_new_bootstrap_holdout_universe,ig_android_cache_layer_bytes_threshold,ig_android_search_hash_tag_and_username_universe,ig_android_business_promotion,ig_android_direct_search_recipients_controller_universe,ig_android_ad_show_full_name_universe,ig_android_anrwatchdog,ig_android_qp_kill_switch,ig_android_2fac,ig_direct_bypass_group_size_limit_universe,ig_android_promote_simplified_flow,ig_android_share_to_whatsapp,ig_android_hide_bottom_nav_bar_on_discover_people,ig_fbns_dump_ids,ig_android_hands_free_before_reverse,ig_android_skywalker_live_event_start_end,ig_android_live_join_comment_ui_change,ig_android_direct_search_story_recipients_universe,ig_android_direct_full_size_gallery_upload,ig_android_ad_browser_gesture_control,ig_channel_server_experiments,ig_android_video_cover_frame_from_original_as_fallback,ig_android_ad_watchinstall_universe,ig_android_ad_viewability_logging_universe,ig_android_new_optic,ig_android_direct_visual_replies,ig_android_stories_search_reel_mentions_universe,ig_android_threaded_comments_universe,ig_android_mark_reel_seen_on_Swipe_forward,ig_internal_ui_for_lazy_loaded_modules_experiment,ig_fbns_shared,ig_android_capture_slowmo_mode,ig_android_live_viewers_list_search_bar,ig_android_video_single_surface,ig_android_offline_reel_feed,ig_android_video_download_logging,ig_android_last_edits,ig_android_exoplayer_4142,ig_android_post_live_viewer_count_privacy_universe,ig_android_activity_feed_click_state,ig_android_snippets_haptic_feedback,ig_android_gl_drawing_marks_after_undo_backing,ig_android_mark_seen_state_on_viewed_impression,ig_android_live_backgrounded_reminder_universe,ig_android_live_hide_viewer_nux_universe,ig_android_live_monotonic_pts,ig_android_search_top_search_surface_universe,ig_android_user_detail_endpoint,ig_android_location_media_count_exp_ig,ig_android_comment_tweaks_universe,ig_android_ad_watchmore_entry_point_universe,ig_android_top_live_notification_universe,ig_android_add_to_last_post,ig_save_insights,ig_android_live_enhanced_end_screen_universe,ig_android_ad_add_counter_to_logging_event,ig_android_blue_token_conversion_universe,ig_android_exoplayer_settings,ig_android_progressive_jpeg,ig_android_offline_story_stickers,ig_android_gqls_typing_indicator,ig_android_chaining_button_tooltip,ig_android_video_prefetch_for_connectivity_type,ig_android_use_exo_cache_for_progressive,ig_android_samsung_app_badging,ig_android_ad_holdout_watchandmore_universe,ig_android_offline_commenting,ig_direct_stories_recipient_picker_button,ig_insights_feedback_channel_universe,ig_android_insta_video_abr_resize,ig_android_insta_video_sound_always_on'''
    SIG_KEY_VERSION = '4'

    def __init__(self, username, password):
        self.islogin = False
        self.follows = []
        self.unfollows = []
        self.countfollower = 0
        self.countfollowing = 0
        self.absorb = 0
        self.follower = 0
        self.unfollow = 0
        self.stutus = [False, False, False, True, False, False]
        self.MaxMin = [80, 800]
        self.FollowHour = 10
        self.ListFollow = []
        self.UnfollowHour = 10
        self.ListUnfollow = []
        self.Listtrun = [False, False, False, False]
        self.Location = []
        self.Hashtag = []
        self.LikeHour = 10
        self.CounterLike = 0
        self.Comment1 = ['سلام', 'ممنون', 'عاليه']
        self.Comment2 = ['مرسي از پست خوبت', 'چه خوبه', 'عالي']
        self.BoolEmoj = False
        self.CommentHour = 5
        self.CounterComment = 0
        m = hashlib.md5()
        m.update(username.encode('utf-8') + password.encode('utf-8'))
        self.device_id = self.generateDeviceId(m.hexdigest())
        self.SetUser(username, password)
        self.isLoggedIn = False
        self.LastResponse = None
        self.next_max_id = ''
        self.NextMaxIdHashtag = ''
        self.NextMaxIdLocation = ''
        self.NextMaxIdFollowings = ''
        self.NextMaxIdFollowers = ''
        #self.rank_tokens = ''

    def SaveToFile(self):
        temp = '[]'
        temp1 = '[]'
        temp2 = '[]'
        temp3 = '[]'
        temp4 = '[]'
        temp5 = '[]'
        temp6 = '[]'
        temp7 = '[]'
        temp8 = '[]'
        temp9 = '[]'
        if (len(self.stutus) != 0):
            temp = '["'
            for i in range(len(self.stutus)):
                if (i != len(self.stutus) - 1):
                    temp += str(self.stutus[i]) + '","'
                else:
                    temp += str(self.stutus[i]) + '"'
            temp += ']'
        if (len(self.ListFollow) != 0):
            temp1 = '["'
            for i in range(len(self.ListFollow)):
                if (i != len(self.ListFollow) - 1):
                    temp1 += str(self.ListFollow[i]) + '","'
                else:
                    temp1 += str(self.ListFollow[i]) + '"'
            temp1 += ']'
        if (len(self.ListUnfollow) != 0):
            temp2 = '["'
            for i in range(len(self.ListUnfollow)):
                if (i != len(self.ListUnfollow) - 1):
                    temp2 += str(self.ListUnfollow[i]) + '","'
                else:
                    temp2 += str(self.ListUnfollow[i]) + '"'
            temp2 += ']'
        if (len(self.Location) != 0):
            temp3 = '["'
            for i in range(len(self.Location)):
                if (i != len(self.Location) - 1):
                    temp3 += str(self.Location[i]) + '","'
                else:
                    temp3 += str(self.Location[i]) + '"'
            temp3 += ']'
        if (len(self.Hashtag) != 0):
            temp4 = '["'
            for i in range(len(self.Hashtag)):
                if (i != len(self.Hashtag) - 1):
                    temp4 += str(self.Hashtag[i]) + '","'
                else:
                    temp4 += str(self.Hashtag[i]) + '"'
            temp4 += ']'
        if (len(self.Comment1) != 0):
            temp5 = '["'
            for i in range(len(self.Comment1)):
                if (i != len(self.Comment1) - 1):
                    temp5 += str(self.Comment1[i]) + '","'
                else:
                    temp5 += str(self.Comment1[i]) + '"'
            temp5 += ']'
        if (len(self.Comment2) != 0):
            temp6 = '["'
            for i in range(len(self.Comment2)):
                if (i != len(self.Comment2) - 1):
                    temp6 += str(self.Comment2[i]) + '","'
                else:
                    temp6 += str(self.Comment2[i]) + '"'
            temp6 += ']'
        if (len(self.follows) != 0):
            temp8 = '["'
            for i in range(len(self.follows)):
                if (i != len(self.follows) - 1):
                    temp8 += str(self.follows[i]) + '","'
                else:
                    temp8 += str(self.follows[i]) + '"'
            temp8 += ']'
        file = '{"username":"' + self.username + '","password":"' + self.password + '","countfollower":"' + str(
            self.countfollower) + '","countfollowing":"' + str(self.countfollowing) + '","absorb":"' + str(
            self.absorb) + '","follower":"' + str(self.follower) + '","unfollow":"' + str(
            self.unfollow) + '","follows":' + temp8 + ',"stutus":' + temp + ',"MaxMin":["' + str(
            self.MaxMin[0]) + '","' + str(self.MaxMin[1]) + '"],' + '"FollowHour":"' + str(
            self.FollowHour) + '","ListFollow":' + temp1 + ',"UnfollowHour":"' + str(
            self.UnfollowHour) + '","ListUnfollow":' + temp2 + ',"Location":' + temp3 + ',"Hashtag":' + temp4 + ',"LikeHour":"' + str(
            self.LikeHour) + '","CounterLike":"' + str(
            self.CounterLike) + '","Comment1":' + temp5 + ',"Comment2":' + temp6 + ',"BoolEmoj":"' + str(
            self.BoolEmoj) + '","CommentHour":"' + str(self.CommentHour) + '","CounterComment":"' + str(
            self.CounterComment) + '"}'
        struct = json.loads(file)
        temp = (str(struct)).replace('\'', '\\\'')
        return temp

    def Get(self, struct):
        self.SetUser(struct['username'], struct['password'])
        self.countfollower = int(struct['countfollower'])
        self.countfollowing = int(struct['countfollowing'])
        self.absorb = int(struct['absorb'])
        self.follower = int(struct['follower'])
        self.unfollow = int(struct['unfollow'])
        self.follows = struct['follows']
        self.stutus[0] = eval((struct['stutus'][0]))
        self.stutus[1] = eval((struct['stutus'][1]))
        self.stutus[2] = eval((struct['stutus'][2]))
        self.stutus[3] = eval((struct['stutus'][3]))
        self.stutus[4] = eval((struct['stutus'][4]))
        self.stutus[5] = eval((struct['stutus'][5]))
        self.MaxMin[0] = int(struct['MaxMin'][0])
        self.MaxMin[1] = int(struct['MaxMin'][1])
        self.FollowHour = int(struct['FollowHour'])
        self.ListFollow = struct['ListFollow']
        self.UnfollowHour = int(struct['UnfollowHour'])
        self.ListUnfollow = struct['ListUnfollow']
        self.Location = struct['Location']
        self.Hashtag = struct['Hashtag']
        self.LikeHour = int(struct['LikeHour'])
        self.CounterLike = int(struct['CounterLike'])
        self.Comment1 = struct['Comment1']
        self.Comment2 = struct['Comment2']
        self.BoolEmoj = eval(struct['BoolEmoj'])
        self.CommentHour = int(struct['CommentHour'])
        self.CounterComment = int(struct['CounterComment'])

    def Show(self):
        global id
        app.insertrow(self.username, self.countfollower, self.countfollowing, self.follower, self.unfollow, self.absorb)
        id = id + 1

    def generateDeviceId(self, seed):
        volatile_seed = "12345"
        m = hashlib.md5()
        m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
        return 'android-' + m.hexdigest()[:16]

    def SetUser(self, username, password):
        self.username = username
        self.password = password
        self.uuid = self.generateUUID(True)

    def generateUUID(self, type):
        generated_uuid = str(uuid.uuid4())
        if (type):
            return generated_uuid
        else:
            return generated_uuid.replace('-', '')

    def Login(self):
        print("in func Login ")
        #global rank_tokens
        if (not self.isLoggedIn):
            self.s = requests.Session()
            if (self.SendRequest('si/fetch_headers/?challenge_type=signup&guid=', None, True)):
                data = {'phone_id': self.generateUUID(True),
                        '_csrftoken': self.LastResponse.cookies['csrftoken'],
                        'username': self.username,
                        'guid': self.uuid,
                        'device_id': self.device_id,
                        'password': self.password,
                        'login_attempt_count': '0'}
                if (self.SendRequest('accounts/login/', self.generateSignature(json.dumps(data)), True)):
                    print("in selfRequset")
                    self.isLoggedIn = True
                    self.username_id = self.LastJson["logged_in_user"]["pk"]
                    self.rank_token = "%s_%s" % (self.username_id, self.uuid)
                    #print("rank_token------:",self.rank_token)
                    self.token = self.LastResponse.cookies["csrftoken"]
                    self.getUsernameInfo(self.username_id)
                    self.countfollower = self.set_follower()
                    self.countfollowing = self.set_following()
                    self.islogin = True
                    print(self.username, " login")
                    return True;
                else:
                    return False

    def generateSignature(self, data):
        try:
            parsedData = urllib.parse.quote(data)
        except AttributeError:
            parsedData = urllib.quote(data)
        return 'ig_sig_key_version=' + self.SIG_KEY_VERSION + '&signed_body=' + hmac.new(
            self.IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest() + '.' + parsedData

    def SendRequest(self, endpoint, post=None,Login=False):
        response = None
        self.s.headers.update({'Connection': 'close',
                                'Accept': '*/*',
                                'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                'Cookie2': '$Version=1',
                                'Accept-Language': 'en-US',
                                'User-Agent': self.USER_AGENT})
        if (post != None):
            response = self.s.post(self.API_URL + endpoint, data=post)
        else:
            try:
                response = self.s.get(self.API_URL + endpoint, timeout=40)
            except requests.exceptions.Timeout:
                print("Timeout occurred")
        if response.status_code == 200:
            self.LastResponse = response
            self.LastJson = response.json()
            return True
        else:
            print("Request return " + str(response.status_code) + " error!")
            print(response.text)
            if response.status_code == 400:
                error = json.loads(response.text)
                if ('feedback_url' in error):
                    if (error['feedback_url'] == 'repute/report_problem/instagram_comment/'):
                        return False
                    elif (error['feedback_url'] == 'repute/report_problem/instagram_like_add/'):
                        return False
            elif response.status_code == 429:
                error = ast.literal_eval(response.text)
                if ("message" in error):
                    print('error429', error['message'])
                    if (error['message'] == 'Please wait a few minutes before you try again.'):
                        LogWrite(
                            'Error 429:Please wait a few minutes before you try again(for user ' + self.username + ' )\n')
                        time.sleep(30)
                        if (post != None):
                            response = self.s.post(self.API_URL + endpoint, data=post)
                        else:
                            response = self.s.get(self.API_URL + endpoint)
                    else:
                        print('exit')
            return False

    def returnselfuserid(self):
        return self.username_id

    def ReturnUserid(self, usernameName):
        self.SendRequest('users/' + str(usernameName) + '/usernameinfo/')
        temp = self.LastJson
        return self.LastJson['user']['pk']

    def BMP(self, s):
        return "".join((i if ord(i) < 10000 else '\ufffd' for i in s))

    # Followers
    def getUserFollowers(self, usernameId, maxid=''):
        #self.rank_token=self.rank_tokens
        if maxid == '':
            return self.SendRequest('friendships/' + str(usernameId) + '/followers/?rank_token=' + self.rank_token)
        else:
            return self.SendRequest(
                'friendships/' + str(usernameId) + '/followers/?rank_token=' + self.rank_token + '&max_id=' + str(
                    maxid))

    def getTotalFollowers(self, usernameId):

        print("in def get total follower")
        follower = []
        pk_follower = []
        username = []
        is_private = []
        has_anonymous_profile_picture = []
        next_max_id = ''
        while 1:
            self.getUserFollowers(usernameId, next_max_id)
            temp = self.LastJson
            if ('big_list' not in temp.keys()):
                return False
            for item in temp['users']:
                #pk_follower.append(item['pk'])
                username.append(item['username'])
                is_private.append(item['is_private'])
                has_anonymous_profile_picture.append(item['has_anonymous_profile_picture'])
            if temp['big_list'] == False:
                print("if big list")
                follower.append(pk_follower)
                follower.append(username)
                follower.append(is_private)
                follower.append(has_anonymous_profile_picture)
                #pk_follower=follower[0]
                #print(pk_follower)

                #new_follower=instagram_follower(pk_follower=follower[0],username=follower[1])
                #new_follower.save()
                print(follower[1])
                print(follower[0])
                #return follower
            next_max_id = temp['next_max_id']

    def getTotalFollowers1(self, usernameId):
        follower = []
        pk = []
        username = []
        is_private = []
        has_anonymous_profile_picture = []
        self.getUserFollowers(usernameId, self.NextMaxIdFollowers)
        temp = self.LastJson

        if ('big_list' not in temp.keys()):
            return False
        if temp['big_list'] == False:
            self.NextMaxIdFollowers = ''
        else:
            self.NextMaxIdFollowers = temp['next_max_id']
        for item in temp['users']:
            pk.append(item['pk'])
            username.append(item['username'])
            is_private.append(item['is_private'])
            has_anonymous_profile_picture.append(item['has_anonymous_profile_picture'])
        follower.append(pk)
        follower.append(username)
        follower.append(is_private)
        follower.append(has_anonymous_profile_picture)
        #print(follower[0])
        #print(follower[1])
        #row = KasfkaCunsumer.objects.all()[0:50]
        #for r in row:
           # r.delete()
        #for i in range(len(follower[0])):
            #new_follower = instagram_follower(pk_follower=follower[0][i], username=follower[1][i])
            #new_follower =instagram_follower.objects.get(pk_follower=follower[0][i],username=follower[1][i])
            #print("pkfollower:",new_follower)
           # if(True):
             #   new_follower=instagram_follower.objects.create(pk_follower=follower[0][i],username=follower[1][i])
                #new_follower=instagram_follower(pk_follower=follower[0][i],username=follower[1][i])
               # new_follower.save()
               # row = instagram_follower.objects.all()
               # for r in row:
                #    if (new_follower == r):
                 #       new_follower.delete()
                #new_follower = instagram_follower.objects.update(pk_follower=follower[0][i], username=follower[1][i])
            #else:
              #  pass



                #new_follower =instagram_follower.objects.update(pk_follower=follower[0][i],username=follower[1][i])
            #new_follower.save()
       # for j in follower[1]:
            #new_follower = instagram_follower(username=j)
            #new_follower.save()

        #print(follower)
        return follower

    def getTotalSelfFollowers(self):
        return self.getTotalFollowers(self.username_id)

    # EndFollowers
    # Followings
    def getUserFollowings(self, usernameId, maxid=''):
        url = 'friendships/' + str(usernameId) + '/following/?'
        query_string = {
            'ig_sig_key_version': self.SIG_KEY_VERSION,
            'rank_token': self.rank_token,
        }
        if maxid:
            query_string['max_id'] = maxid
        if sys.version_info.major == 3:
            url += urllib.parse.urlencode(query_string)
        else:
            url += urllib.urlencode(query_string)
        self.SendRequest(url)

    def getTotalFollowings(self, usernameId):
        following = []
        pk = []
        username = []
        next_max_id = ''
        while 1:
            self.getUserFollowings(usernameId, next_max_id)
            temp = self.LastJson
            for item in temp["users"]:
                pk.append(item['pk'])
                username.append(item['username'])
            if temp["big_list"] == False:
                following.append(pk)
                following.append(username)
                return following
            next_max_id = temp["next_max_id"]

    def getTotalFollowings1(self, usernameId):
        following = []
        pk = []
        username = []
        start = time.time()
        end = 0
        self.getUserFollowings(usernameId, self.NextMaxIdFollowings)
        temp = self.LastJson
        if len(temp["users"]) == 0:
            return False
        while (end - start < 1 or temp["big_list"] != False):
            for item in temp["users"]:
                pk.append(item['pk'])
                username.append(item['username'])
            following.append(pk)
            following.append(username)
            self.getUserFollowings(usernameId, self.NextMaxIdFollowings)
            temp = self.LastJson
            if temp["big_list"] == False:
                self.NextMaxIdFollowings = ''
            else:
                self.NextMaxIdFollowings = temp["next_max_id"]
            end = time.time()
        return following

    def getTotalSelfFollowings(self):
        return self.getTotalFollowings(self.username_id)

    # EndFollowings
    def userFriendship(self, userId):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.username_id,
            'user_id': userId,
            '_csrftoken': self.token
        })
        self.SendRequest('friendships/show/' + str(userId) + '/', self.generateSignature(data))
        temp = self.LastJson
        return (temp['outgoing_request'] or temp['following'])

    def getUsernameInfo(self, usernameId):
        self.SendRequest('users/' + str(usernameId) + '/info/')

    def set_follower(self):
        self.follower_count = self.LastJson["user"]["follower_count"]
        return self.follower_count

    def set_following(self):
        self.following_count = self.LastJson["user"]["following_count"]
        return self.following_count

    def set_profile_pic(self):
        self.profile_pic_url=self.LastJson['user']['profile_pic_url']
        return self.profile_pic_url

    def follow(self, userId):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.username_id,
            'user_id': userId,
            '_csrftoken': self.token
        })
        return self.SendRequest('friendships/create/' + str(userId) + '/', self.generateSignature(data))

    def unfollow1(self, userId):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.username_id,
            'user_id': userId,
            '_csrftoken': self.token
        })
        self.SendRequest('friendships/destroy/' + str(userId) + '/', self.generateSignature(data))

    def like(self, mediaId):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.username_id,
            '_csrftoken': self.token,
            'media_id': mediaId
        })
        return self.SendRequest('media/' + str(mediaId) + '/like/', self.generateSignature(data))

    def comment(self, mediaId, commentText):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.username_id,
            '_csrftoken': self.token,
            'comment_text': commentText
        })
        return self.SendRequest('media/' + str(mediaId) + '/comment/', self.generateSignature(data))

    def getMediaLikers(self, mediaId):
        liker = []
        ids = []
        username = []
        is_private = []
        profile_pic_id = []
        self.SendRequest('media/' + str(mediaId) + '/likers/?')
        temp = self.LastJson
        for item in temp['users']:
            ids.append(item['pk'])
            username.append(item['username'])
            is_private.append(item['is_private'])
            if 'profile_pic_id' in item.keys():
                profile_pic_id.append('False')
            else:
                profile_pic_id.append('True')
        liker.append(ids)
        liker.append(username)
        liker.append(is_private)
        liker.append(profile_pic_id)
        return liker

    def getidpitcure(self, usernameId, maxid='', minTimestamp=None):
        query = self.SendRequest('feed/user/' + str(usernameId) + '/?max_id=' + str(maxid) + '&min_timestamp=' + str(
            minTimestamp) + '&rank_token=' + str(self.rank_token) + '&ranked_content=true')

    def getpitcure(self, usernameId):
        list_pitcure = []
        self.getidpitcure(usernameId, self.next_max_id)
        temp = self.LastJson
        if ('more_available' not in temp.keys()):
            return False
        for item in temp['items']:
            list_pitcure.append(item['id'])
        if temp['more_available'] == False:
            self.next_max_id = ''
        else:
            self.next_max_id = temp['next_max_id']
        return list_pitcure

    def getUserFeed(self, usernameId, maxid='', minTimestamp=None):
        query = self.SendRequest(
            'feed/user/' + str(usernameId) + '/?max_id=' + str(maxid) + '&min_timestamp=' + str(minTimestamp)
            + '&rank_token=' + str(self.rank_token) + '&ranked_content=true')
        if (len(self.LastJson['items']) != 0):
            return self.LastJson['items'][0]['id']
        else:
            return False

    # Location
    def searchLocation(self, query):
        pk = []
        name = []
        location = []
        locationFeed = self.SendRequest('fbsearch/places/?rank_token=' + str(self.rank_token) + '&query=' + str(query))
        temp = self.LastJson
        for item in temp['items']:
            pk.append(item['location']['pk'])
            name.append(item['location']['name'])
        location.append(pk)
        location.append(name)
        return location

    def getLocationFeed(self, locationId, maxid=''):
        return self.SendRequest('feed/location/' + str(
            locationId) + '/?max_id=' + maxid + '&rank_token=' + self.rank_token + '&ranked_content=true&')

    def BMP(self, s):
        return "".join((i if ord(i) < 10000 else '\ufffd' for i in s))

    def getLocation(self, locationId):
        location = []
        pk = []
        username = []
        self.getLocationFeed(locationId, self.NextMaxIdLocation)
        temp = self.LastJson
        if ('more_available' not in temp.keys()):
            return False
        for item in temp['items']:
            pk.append(item['id'])
            username.append(item['user']['username'])
        location.append(pk)
        location.append(username)
        if temp['more_available'] != False:
            self.NextMaxIdLocation = temp['next_max_id']
        else:
            self.NextMaxIdLocation = ''
        return location

    # EndLocation
    # Hashtag
    def getHashtagFeed(self, hashtagString, maxid=''):
        self.SendRequest('feed/tag/' + hashtagString + '/?max_id=' + str(
            maxid) + '&rank_token=' + self.rank_token + '&ranked_content=true&')

    def getHashtag(self, hashtagString):
        hashtag = []
        pk = []
        username = []
        self.getHashtagFeed(hashtagString, self.NextMaxIdHashtag)
        temp = self.LastJson
        if ('more_available' not in temp.keys()):
            return False
        for item in temp['items']:
            pk.append(item['id'])
            username.append(item['user']['username'])
        hashtag.append(pk)
        hashtag.append(username)
        if temp['more_available'] != False:
            self.NextMaxIdHashtag = temp['next_max_id']
        else:
            self.NextMaxIdHashtag = ''
        return hashtag


# class myThread(threading.Thread):
#
#     def __init__(self, threadID):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#
#     def run(self):
#         if (self.threadID == 1):
#             Follow()
#         elif (self.threadID == 2):
#             Unfollow()
#         elif (self.threadID == 3):
#             Hashtag()
#         else:
#             GetInformation()


def Follow():
 global checkfollow
 global terminate
 t=0
 start=0
 end=0
 delay={}
 for user in Users.copy().keys():
       if (UserClass[Users[user][0]].islogin==False):
          UserClass[Users[user][0]].Login()
 while(1):
  if(terminate==1):
      break
  if(bool(Users)==True):
    for user in Users.copy().keys():
     try:
      if (UserClass[Users[user][0]].Listtrun[0]==True and UserClass[Users[user][0]].islogin==True):
       list_follower=[]
       self_following=[]
       if(user not in delay.keys()):
                 delay[user]=[0,0,0]
       delay[user][1]=time.time()
       if(delay[user][2]==1):
            temp=3600/((UserClass[Users[user][0]]).FollowHour)
            if((delay[user][1]-delay[user][0])<temp):
               continue
       list_user_follow=(UserClass[Users[user][0]]).ListFollow[:]
       like=(UserClass[Users[user][0]]).stutus[0]
       private_account=((UserClass[Users[user][0]]).stutus[2])
       pitcure_account=((UserClass[Users[user][0]]).stutus[1])
       min_follower=int((UserClass[Users[user][0]]).MaxMin[0])
       max_follower=int((UserClass[Users[user][0]]).MaxMin[1])
       hour_follow=(UserClass[Users[user][0]]).FollowHour
       if((UserClass[Users[user][0]]).stutus[3]==True):
           stutus_follow=1
       elif((UserClass[Users[user][0]]).stutus[4]==True):
           stutus_follow=2
       else:
           t=randint(0,1)
           stutus_follow=3
       if(stutus_follow==1 or (stutus_follow==3 and t==0)):
         index=[]
         for i in range(len(list_user_follow)):
              userid=UserClass[Users[user][0]].ReturnUserid(list_user_follow[i])
              follower=UserClass[Users[user][0]].getTotalFollowers1(userid)
              if(follower!=False):
                    list_follower.append(follower)
              else:
                    index.append(i)
         for i in range(len(index)):
                list_user_follow.remove(list_user_follow[index[i]])
                for j in range(i+1,len(index)):
                    index[j]-=1
       else:
            list_id_pitcure=[]
            index=[]
            list_temp=[]
            for i in range(len(list_user_follow)):
              userid=UserClass[Users[user][0]].ReturnUserid(list_user_follow[i])
              idpitcure=UserClass[Users[user][0]].getpitcure(userid)
              if(idpitcure!=False):
                    list_id_pitcure.append(idpitcure)
              else:
                    index.append(i)
            for i in range(len(index)):
                list_user_follow.remove(list_user_follow[index[i]])
                for j in range(i+1,len(index)):
                    index[j]-=1
            for i in range(len(list_user_follow)):
                 list_temp=[]
                 ran=randint(0, len(list_id_pitcure[i])-1)
                 liker=UserClass[Users[user][0]].getMediaLikers(str(list_id_pitcure[i][ran]))
                 list_follower.append(liker)
       for i in range(len(list_user_follow)):
           time1=time.time()
           while(1):
              time2=time.time()
              if(time2-time1>10):
                  break
              if(len(list_follower[i][0])==0):
                   break
              ran=randint(0, len(list_follower[i][0])-1)
              userid=UserClass[Users[user][0]].returnselfuserid()
              if(userid==list_follower[i][0][ran]  or UserClass[Users[user][0]].userFriendship(list_follower[i][0][ran])):
                  del(list_follower[i][0][ran])
                  del(list_follower[i][1][ran])
                  del(list_follower[i][2][ran])
                  del(list_follower[i][3][ran])
                  continue
              UserClass[Users[user][0]].getUsernameInfo(list_follower[i][0][ran])
              counter_follower=UserClass[Users[user][0]].set_follower()
              if(counter_follower>=min_follower and counter_follower<=max_follower):
                  t1=t2=1
                  if(private_account==True):
                      if(list_follower[i][2][ran]==True):
                        t1=0
                  if(pitcure_account==True):
                      if(list_follower[i][3][ran]==True):
                        t2=0
                  if(t1==1 and t2==1):
                     if(list_follower[i][2][ran]==False):
                        UserClass[Users[user][0]].follow(str(list_follower[i][0][ran]))
                        LogWrite(user+' started follow '+list_follower[i][1][ran]+'\n')
                        UserClass[Users[user][0]].follower+=1
                        print(user,' started follow ',list_follower[i][1][ran],'\n')
                        if(like==True):
                                mediaid=UserClass[Users[user][0]].getUserFeed(str(list_follower[i][0][ran]))
                                if(mediaid!=False):
                                    liker=UserClass[Users[user][0]].getMediaLikers(mediaid)
                                    if(user not in liker[1]):
                                        stutus=UserClass[Users[user][0]].like(str(mediaid))
                                        if(stutus!=False):
                                            LogWrite(user+' like page '+list_follower[i][1][ran]+'\n')
                                            print(user,' like page ',list_follower[i][1][ran],'\n')
                                        else:
                                            print(user+' can not like post '+str(list_follower[i][1][ran])+'\n')
                                            LogWrite(user+' can not like  post '+str(list_follower[i][1][ran])+'\n')
                     else:
                        UserClass[Users[user][0]].follow(str(list_follower[i][0][ran]))
                        LogWrite(user+' started follow '+list_follower[i][1][ran]+'  (by requested)\n')
                        print(user,' started follow ',list_follower[i][1][ran],' (by requested)\n')
                     UserClass[Users[user][0]].follower+=1
                     UserClass[Users[user][0]].follows.append(list_follower[i][0][ran])
                     delay[user][2]=1
                     delay[user][0]=time.time()
                     break
              del(list_follower[i][0][ran])
              del(list_follower[i][1][ran])
              del(list_follower[i][2][ran])
              del(list_follower[i][3][ran])
     except Exception as e:
        print(str(e),'\n')
        continue
  time.sleep(1)
# bot.getSelfUsersFollowing()
# bot.getSelfUserFollowers()
# bot.searchLocation("kashan")/////
# bot.getLocationFeed(locationId=230111197)
# bot.getTotalSelfFollowers()

