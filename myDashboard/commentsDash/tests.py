from __future__ import annotations

from django.core.cache import cache
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from .utils.utils import get_all_video_ids_in_cache
from .utils.utils import url_to_videoId_parser
from .utils.youCom import commentsAnalysis


# Test video parse of coverting youtube url to video_id
class Video_id_Tests(TestCase):
    def test_valid_urls(self):
        valid_url_list = [
            'http://www.youtube.com/watch?v=0zM3nApSvMg&feature=feedrec_grec_index',
            'http://www.youtube.com/user/IngridMichaelsonVEVO#p/a/u/1/0zM3nApSvMg',
            'http://www.youtube.com/v/0zM3nApSvMg?fs=1&amp;hl=en_US&amp;rel=0',
            'http://www.youtube.com/watch?v=0zM3nApSvMg#t=0m10s',
            'http://www.youtube.com/embed/0zM3nApSvMg?rel=0',
            'http://www.youtube.co.uk/watch?v=0zM3nApSvMg',
            'http://youtu.be/0zM3nApSvMg',
        ]

        self.assertTrue(
            url_to_videoId_parser(
                valid_url_list[0],
            ) == '0zM3nApSvMg',
        )
        self.assertTrue(
            url_to_videoId_parser(
                valid_url_list[1],
            ) == '0zM3nApSvMg',
        )
        self.assertTrue(
            url_to_videoId_parser(
                valid_url_list[2],
            ) == '0zM3nApSvMg',
        )
        self.assertTrue(
            url_to_videoId_parser(
                valid_url_list[3],
            ) == '0zM3nApSvMg',
        )
        self.assertTrue(
            url_to_videoId_parser(
                valid_url_list[4],
            ) == '0zM3nApSvMg',
        )
        self.assertTrue(
            url_to_videoId_parser(
                valid_url_list[5],
            ) == '0zM3nApSvMg',
        )
        self.assertTrue(
            url_to_videoId_parser(
                valid_url_list[6],
            ) == '0zM3nApSvMg',
        )

    # Test invalid urls of youtube videos
    def test_invalid_urls(self):
        invalid_url_list = [
            'http://www.youtube/watch?v=nApSvMg&feature=feedrec_grec_index',
            'http://www.amazon.com/user/IngridMichaelsonVEVO#p/a/u/1/0zasM3nApSvMg',
            'http://wwww.youtube.com/v/AAAAAAAA?fs=1&amp;hl=en_US&amp;relzxczxc=0dadsadas',
            '0zM3nApSvMg',
            'http://www.youtube.co.uk/watchs?v=0zM3nApSvMgs',
            'htttp://www.youtube.com/embedfaketesting/0zM3nApSvMg?rel=0',
            'http://www.youtube.co.uk/watchs?v=0zM3nApSvMg',
            'http://youtu.ee/0zM3nApSvMg',
        ]

        self.assertFalse(
            url_to_videoId_parser(
                invalid_url_list[0],
            ) == '0zM3nApSvMg',
        )
        self.assertFalse(
            url_to_videoId_parser(
                invalid_url_list[1],
            ) == '0zM3nApSvMg',
        )
        self.assertFalse(
            url_to_videoId_parser(
                invalid_url_list[2],
            ) == '0zM3nApSvMg',
        )
        self.assertFalse(
            url_to_videoId_parser(
                invalid_url_list[3],
            ) == '0zM3nApSvMg',
        )
        self.assertFalse(
            url_to_videoId_parser(
                invalid_url_list[4],
            ) == '0zM3nApSvMg',
        )
        self.assertFalse(
            url_to_videoId_parser(
                invalid_url_list[5],
            ) == '0zM3nApSvMg',
        )
        self.assertFalse(
            url_to_videoId_parser(
                invalid_url_list[6],
            ) == '0zM3nApSvMg',
        )
        self.assertFalse(
            url_to_videoId_parser(
                invalid_url_list[7],
            ) == '0zM3nApSvMg',
        )


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()  # Initialize the test client

    # Test Index View
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/index.html')

    # Test analysis View with valid url
    def test_valid_url_dashboard_view(self):
        video_id = url_to_videoId_parser(
            'http://www.youtube.com/embed/0zM3nApSvMg?rel=0',
        )
        response = self.client.get(reverse('analysis', args=[video_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/dashboard.html')

    # Test analysis View with invalid url
    def test_invalid_url_dashboard_view(self):
        video_id = url_to_videoId_parser(
            'http://www.youtube.co.uk/watchs?v=0zM3nApSvMgs',
        )
        response = self.client.get(reverse('analysis', args=[video_id]))
        self.assertTemplateUsed(response, 'html/index.html')


class YouTubeCommentsTests(TestCase):
    def setUp(self):
        self.video_id = '0zM3nApSvMg'
        self.results, self.meta = commentsAnalysis(self.video_id)

    # Test if the comments retrieved are from the intended video
    def test_correct_video_retrieval(self):
        self.assertEqual(self.video_id, self.meta['video_id'])

    # Test against the maximum number of comments
    def test_max_number_comments(self):
        self.assertLessEqual(len(self.results), 200)

    # Test for the correct metadata
    def test_meta_data(self):
        self.assertEqual(len(self.meta.keys()), 12)

    # Test for storing cache video
    def test_cache_length(self):
        self.assertEqual(len(get_all_video_ids_in_cache()), 1)

    # Test the cache when a new video is searched
    # Test for the correct contents of the cache

    def test_cache_length_with_new_video_id(self):
        video_id = 'rMmfK4_u1Cc'
        commentsAnalysis(video_id)
        self.assertEqual(len(get_all_video_ids_in_cache()), 1)
        self.assertEqual(cache.get(get_all_video_ids_in_cache()), None)
