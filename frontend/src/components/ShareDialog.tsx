import React, { useState, useEffect } from 'react';
import { getShareLink } from '../lib/api';
import { ShareData } from '../lib/api';
import { toast } from 'react-hot-toast';

interface ShareDialogProps {
  storyId: number;
  isOpen: boolean;
  onClose: () => void;
}

const ShareDialog: React.FC<ShareDialogProps> = ({ storyId, isOpen, onClose }) => {
  const [shareData, setShareData] = useState<ShareData | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen && storyId) {
      fetchShareData();
    }
  }, [isOpen, storyId]);

  const fetchShareData = async () => {
    try {
      setLoading(true);
      const data = await getShareLink(storyId);
      setShareData(data);
    } catch (error) {
      console.error('Error fetching share data:', error);
      toast.error('Failed to generate share link');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    if (shareData) {
      navigator.clipboard.writeText(shareData.shareUrl);
      toast.success('Link copied to clipboard!');
    }
  };

  const shareOnSocial = (platform: string) => {
    if (!shareData) return;

    const text = `Check out this story: ${shareData.shareData.title}`;
    const url = encodeURIComponent(shareData.shareUrl);

    let shareUrl = '';
    switch (platform) {
      case 'twitter':
        shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${url}`;
        break;
      case 'facebook':
        shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
        break;
      case 'linkedin':
        shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${url}`;
        break;
      case 'whatsapp':
        shareUrl = `https://wa.me/?text=${encodeURIComponent(text + ' ' + shareData.shareUrl)}`;
        break;
    }

    window.open(shareUrl, '_blank');
  };

  if (!isOpen) return null;

  return (
    <div className="share-dialog-overlay" onClick={onClose}>
      <div className="share-dialog" onClick={e => e.stopPropagation()}>
        <div className="share-dialog-header">
          <h3>Share Story</h3>
          <button className="close-button" onClick={onClose}>×</button>
        </div>

        <div className="share-dialog-content">
          {loading ? (
            <div className="loading">Generating share link...</div>
          ) : shareData ? (
            <>
              <div className="share-url">
                <input 
                  type="text" 
                  value={shareData.shareUrl} 
                  readOnly 
                  className="share-url-input"
                />
                <button 
                  onClick={copyToClipboard}
                  className="copy-button"
                >
                  Copy
                </button>
              </div>

              <div className="social-share-buttons">
                <button 
                  onClick={() => shareOnSocial('twitter')}
                  className="social-button twitter"
                >
                  <span className="social-icon">🐦</span> Twitter
                </button>
                <button 
                  onClick={() => shareOnSocial('facebook')}
                  className="social-button facebook"
                >
                  <span className="social-icon">📘</span> Facebook
                </button>
                <button 
                  onClick={() => shareOnSocial('linkedin')}
                  className="social-button linkedin"
                >
                  <span className="social-icon">💼</span> LinkedIn
                </button>
                <button 
                  onClick={() => shareOnSocial('whatsapp')}
                  className="social-button whatsapp"
                >
                  <span className="social-icon">💬</span> WhatsApp
                </button>
              </div>
            </>
          ) : (
            <div className="error">Failed to generate share link</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ShareDialog; 