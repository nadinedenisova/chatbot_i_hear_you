import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import ImageListItemBar from '@mui/material/ImageListItemBar';
import IconButton from '@mui/material/IconButton';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import VideoLibraryIcon from '@mui/icons-material/VideoLibrary';
import MoreVertIcon from '@mui/icons-material/MoreVert';

// TODO Заменить моковые данные
export default function AttachmentList() {
  return (
    <>
      <ImageList cols={5} gap={5} rowHeight={200}>
        {itemData.map((item) => (
          <ImageListItem key={item.img}>
            <img
              srcSet={`${item.img}?w=248&fit=crop&auto=format&dpr=2 2x`}
              src={`${item.img}?w=248&fit=crop&auto=format`}
              alt={item.title}
              loading="lazy"
            />
            <ImageListItemBar
              title={item.title}
              actionIcon={
                <IconButton
                  sx={{ color: 'rgba(255, 255, 255, 0.54)' }}
                  aria-label={`info about ${item.title}`}
                >
                  <MoreVertIcon />
                </IconButton>
              }
            />
          </ImageListItem>
        ))}

        <ImageListItem>
          <PictureAsPdfIcon sx={{ width: '90%', height: '90%' }} />
          <ImageListItemBar
            title={'Список вопросов.pdf'}
            actionIcon={
              <IconButton
                sx={{ color: 'rgba(255, 255, 255, 0.54)' }}
                aria-label={'Я волнуюсь о слухе своего ребенка'}
              >
                <MoreVertIcon />
              </IconButton>
            }
          />
        </ImageListItem>
        <ImageListItem>
          <VideoLibraryIcon sx={{ width: '90%', height: '90%' }} />
          <ImageListItemBar
            title={'Подкаст.mp4'}
            actionIcon={
              <IconButton
                sx={{ color: 'rgba(255, 255, 255, 0.54)' }}
                aria-label={'Как начинать'}
              >
                <MoreVertIcon />
              </IconButton>
            }
          />
        </ImageListItem>
      </ImageList>
    </>
  );
}

const itemData = [
  {
    img: 'https://www.ihearyou.ru/upload/iblock/ad7/vtb5o6j1ou54vdoi6zxyqeped88g7flc.jpg',
    title: 'Я волнуюсь о слухе своего ребенка',
  },
  {
    img: 'https://www.ihearyou.ru/upload/iblock/a5b/3bf1penc4jrtdc2t462vwc83m8noj2ec.png',
    title: 'Как начинать',
  },
  {
    img: 'https://www.ihearyou.ru/upload/iblock/ebc/171vm5z6ej5kz3mthat8zn0xb293flf6.jpg',
    title: 'Как принять диагноз',
  },
];
