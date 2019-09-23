new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    data: {
        query: '다이어트',
        start: 0,
        first_page_doc_number: 20,
        page_doc_number: 30,
        documents: [],
        page: 0,
        max_page: 5
    },
    mounted() {
        this.scroll();
    },
    methods: {
        pressSearchBtn: function () {
            this.page = 0;
            this.start = 0;
            this.documents = [];
            this._callSearchApi(this.query, 0, this.first_page_doc_number)
        },

        _callSearchApi: function (query, start, number) {
            let url = '/search?q=' + query;
            url += '&s=' + start;
            url += '&n=' + number;

            let self = this;
            axios.get(url)
                .then(function (response) {
                    let _docs = self.documents;
                    response['data']['documents'].forEach(function (rr) {
                        let dd = {};
                        dd['channel_id'] = rr['channel_id'];
                        dd['channel_name'] = rr['channel_name'];
                        dd['channel_url'] = 'https://www.youtube.com/channel/' + rr['channel_id'];
                        dd['rating'] = rr['rating'];
                        dd['title'] = rr['title'];
                        dd['video_id'] = rr['video_id'];
                        dd['views'] = rr['views'];
                        dd['img_url'] = 'https://img.youtube.com/vi/' + rr['video_id'] + '/maxresdefault.jpg';
                        dd['url'] = 'https://www.youtube.com/watch?v=' + rr['video_id'];
                        dd['summary'] = rr['summary'];
                        _docs.push(dd)
                    });

                });
        },

        displayViews: function (views) {
            if (views > 10000) {
                let num = views / 10000;
                if (num < 10) {
                    return num.toFixed(1) + '만회';
                } else {
                    return num.toFixed() + '만회';
                }

            }
            if (views > 1000) {
                let num = views / 1000;
                if (num < 1000) {
                    return num.toFixed(1) + '만회';
                } else {
                    return num.toFixed() + '만회';
                }
            }
        },

        scroll() {
            window.onscroll = () => {
                let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight > (document.documentElement.offsetHeight - 10);
                if (bottomOfWindow) {
                    let self = this;
                    setTimeout(function () {
                            if (self.page >= self.max_page) {
                                console.log('Sorry this is last page!')
                            } else {

                                if (self.page === 0) {
                                    self.start = self.start + self.first_page_doc_number;
                                } else {
                                    self.start = self.start + self.page_doc_number
                                }

                                self._callSearchApi(self.query, self.start, self.page_doc_number);
                                self.page += 1;
                            }
                        }
                        , 1500);
                }
            }
        }
    }
});

